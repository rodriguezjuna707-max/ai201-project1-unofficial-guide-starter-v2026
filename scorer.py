"""
The judge. Unit 2.

`run_eval.py` finds this file on its own and calls `judge` once per question
per run, so the Run columns in results/ carry pass/fail instead of raw text.

The point of writing it down as code rather than reading the answers myself is
repeatability: I scored two questions differently on two different days when I
was doing it by eye. A function gets the same answer every time, and when it is
wrong it is wrong in a way I can see and fix.

WHAT EACH CHECK MEASURES — these map one to one onto criteria.md:

  criterion 1  `retrieval_hit`   the `expects` phrase is in a retrieved chunk
  criterion 2  `names_source`    the answer names a file that really exists
  criterion 5  `citation_right`  a file it named actually contains `expects`

Criterion 3 (the gate) is not in here. `run_eval.py::check_out_of_scope`
measures it in one deterministic pass and writes it into the run log itself.
Criterion 4 is about chunks, not answers, and nothing in an answer can show it.

`judge` is the conjunction of all three plus `answer_right`, so a "pass" in the
run log means the whole chain held for that run: the answer was in what came
back, the model used it, it named a source, and the source it named was one
that actually says so.

KNOWN LIMITATION, on purpose. Every check is a substring match against the
`expects` string I wrote in `questions.py` before I saw any output. So the
judge reads "$1.25" but not "1.25", and "8am to 11am" but not "8:00–11:00".
When it marks something wrong that I can see is right, that is a bug in this
file to fix here — not a number to quietly overwrite in the run log.
"""

import re
import unicodedata

import config

# gate.py's exact wording. A refused question produced no answer, so every
# answer-level check below is False for it rather than accidentally true.
REFUSAL = "I don't have enough information about that."

# Sources are cited by filename. Every document in the corpus is a .txt.
_SOURCE_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_\-]*\.txt")

_corpus_cache: dict[str, str] | None = None


def normalise(text: str) -> str:
    """
    Flatten the cosmetic differences between two runs saying the same thing.

    The model writes a filename as `course_biol_160.txt` on one run and bare on
    the next, and an en dash where I typed a hyphen. None of that is the thing
    I am measuring, so it goes before anything is compared.
    """
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("`", "").replace("*", "")
    text = text.translate(str.maketrans({"–": "-", "—": "-", "’": "'", "‘": "'",
                                         "“": '"', "”": '"'}))
    return re.sub(r"\s+", " ", text).strip().lower()


def _corpus() -> dict[str, str]:
    """Every document in the corpus, normalised, keyed by filename.

    Criterion 5 asks whether the file the answer *cited* contains the fact. The
    retrieved chunks can't answer that — top-k is 3, so a file can be cited and
    its relevant chunk not be in `results`. The file on disk can.
    """
    global _corpus_cache
    if _corpus_cache is None:
        _corpus_cache = {
            path.name: normalise(path.read_text(encoding="utf-8"))
            for path in sorted(config.corpus_path().glob("*.txt"))
        }
    return _corpus_cache


def cited_sources(answer: str) -> list[str]:
    """The filenames an answer names, in the order it names them."""
    seen: list[str] = []
    for name in _SOURCE_RE.findall(normalise(answer)):
        if name not in seen:
            seen.append(name)
    return seen


def refused(answer: str) -> bool:
    return normalise(answer) == normalise(REFUSAL)


# ─── criterion 1 ─────────────────────────────────────────────────────────────

def retrieval_hit(expects: str, results) -> bool:
    """Did a chunk containing the answer actually come back?

    This one never varies between runs — retrieval is deterministic — so the
    three Run columns agreeing on it is the expected result, not a copy-paste.
    """
    if not expects:
        return False
    needle = normalise(expects)
    return any(needle in normalise(r.text) for r in results or [])


# ─── criterion 2 ─────────────────────────────────────────────────────────────

def names_source(answer: str) -> bool:
    """Does the answer name at least one document that exists?

    Existence matters. An answer that cites `campus_housing_guide.txt`, which
    is not in the corpus, has not named a source — it has invented one, and
    that is worse than naming none.
    """
    if refused(answer):
        return False
    corpus = _corpus()
    return any(name in corpus for name in cited_sources(answer))


# ─── criterion 5 ─────────────────────────────────────────────────────────────

def citation_right(expects: str, answer: str) -> bool:
    """Does a file the answer named actually contain the fact?

    The failure this is watching for: BIOL 160 has three files and the seven
    laundry files are near identical, so citing the sibling — true-sounding,
    wrong file — costs nothing unless something checks.
    """
    if not expects or refused(answer):
        return False
    corpus = _corpus()
    needle = normalise(expects)
    return any(needle in corpus.get(name, "") for name in cited_sources(answer))


# ─── the answer itself ───────────────────────────────────────────────────────

def answer_right(expects: str, answer: str) -> bool:
    """Did the answer state the fact? Retrieval can hit and the model still miss."""
    if not expects or refused(answer):
        return False
    return normalise(expects) in normalise(answer)


# ─── what run_eval.py calls ──────────────────────────────────────────────────

def score(question: str, expects: str, answer: str, results) -> dict:
    """Every check for one run, so the run log can be aggregated per criterion."""
    return {
        "c1_retrieval_hit": retrieval_hit(expects, results),
        "c2_names_source": names_source(answer),
        "c5_citation_right": citation_right(expects, answer),
        "answer_right": answer_right(expects, answer),
        "cited": cited_sources(answer),
        "refused": refused(answer),
    }


def judge(question, expects: str, answer, results) -> bool:
    """One run of one question: did the whole chain hold?"""
    marks = score(question, expects, answer, results)
    return all(marks[k] for k in
               ("c1_retrieval_hit", "c2_names_source", "c5_citation_right", "answer_right"))
