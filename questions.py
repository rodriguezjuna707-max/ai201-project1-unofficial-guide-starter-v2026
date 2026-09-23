"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # Every `expects` below is a literal string from the corpus, so I can check
    # it with a substring match instead of re-reading an answer and deciding how
    # I feel about it. The file each one lives in is noted for criterion 5.
    {
        # 7 buildings have a laundry file and they are near identical apart from
        # the prices. $1.25 is the only dry price that belongs to one building,
        # so a wrong dorm is visible in the answer. This is the one I expect to
        # miss under criterion 1.
        # housing_morrow_house_laundry.txt, housing_morrow_house.txt
        "question": "How much does a dryer cost in Morrow House?",
        "expects": "$1.25",
    },
    {
        # The opposite case: this number is in one file out of 88.
        # admin_printing_quota.txt
        "question": "How many black and white pages does the printing quota cover?",
        "expects": "600",
    },
    {
        # One file, and also the nearest neighbour to the ibuprofen question in
        # OUT_OF_SCOPE, which is why criterion 3 is 4 of 5 and not 5 of 5.
        # health_center.txt
        "question": "When are the walk in hours at the health centre?",
        "expects": "8am to 11am",
    },
    {
        # Shares "week six" with admin_withdrawal_deadline.txt, which is a
        # different deadline. Tests whether retrieval separates two policies
        # that use the same words.
        # admin_add_drop_deadline.txt
        "question": "How late in the term can I drop a course?",
        "expects": "week six",
    },
    {
        # BIOL 160 has three files and this fact sits in two of them. Both are
        # honest sources, so criterion 5 passes on either; citing the third one,
        # course_biol_160_exams.txt, is the failure it is looking for.
        # course_biol_160.txt, course_biol_160_workload.txt
        "question": "How many hours a week does BIOL 160 take?",
        "expects": "9 to 11 hours",
    },
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
