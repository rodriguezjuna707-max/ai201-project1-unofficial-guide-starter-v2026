# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The corpus is `campus_life`: 88 short posts about one university, written the
way students actually talk to each other. Dorms, dining halls, courses, and
registrar policy.

It answers specific factual questions that have one right answer. What a dryer
costs in Morrow House, how late you can drop a course, how many hours a week
BIOL 160 takes. It retrieves the three closest chunks, answers only from those,
and names the file it used. If nothing is close enough it says it doesn't have
enough information instead of guessing.

## Chunking Strategy

**Chunk size:** 450 characters max, 100 min, split on paragraph breaks
**Overlap:** none. I repeat the document's title line in every chunk instead.

**What I noticed.** `python app.py index` told me the starter wasn't chunking
anything: 88 documents in, 88 chunks out. My longest document is 549 characters
and the starter cuts at 800, so it never fired once. That sounds fine until you
read one. `housing_old_brewhouse.txt` is 550 characters covering the building's
history, the heating, the laundry prices, and the noise. Ask about noise and
the chunk you get back is mostly about heating. One file was not one thought.

So I split on the blank lines the writers already put in, because those breaks
are topical here: one paragraph is the heating, the next is the laundry. That
took me from 88 chunks to 135, and 41 of the 88 documents now split.

**Why 450.** I picked 400 first, then measured the paragraphs: the longest is
373 characters and the longest title is 47. At 400 those two together would
have forced a paragraph apart, which is the one thing this chunker exists to
prevent. 450 is the smallest ceiling that never cuts anything here.

**Why a 100 floor.** Paragraphs run about 80 to 150 characters, so splitting on
every blank line alone makes fragments. Anything under 100 in this corpus is a
heading or a one line aside, so it gets merged into the paragraph after it.

**Why no overlap.** Every document names its subject once, in the title line,
and never again. The body of `housing_old_brewhouse.txt` says "the heating is
uneven" without saying which building, and there are 21 housing files. That is
the real problem overlap was meant to solve, so I solved it directly by
repeating the title in every chunk. It costs about 30 characters instead of
120, and it doesn't manufacture more near duplicates in a corpus that already
has seven nearly identical laundry files.

## Sample Chunks

Printed by `python app.py chunks -n 5`. All five produced by
`chunker.py::split_documents`.

**Chunk 1** | source: `admin_add_drop_deadline.txt#0` | produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript. Nothing anywhere on the registrar's site says this plainly,
and students find out from each other.
```

Stands alone. Both deadlines and the penalty are in it.

**Chunk 2** | source: `course_cs_340.txt#0` | produced by: `chunker.py::split_documents`

```
CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus
a project that runs the whole term. Assessment: one midterm and a final, both
open-book. Lightly curved, usually two or three points.
```

Stands alone, and the course code is in it. That matters because CS 210 is a
near twin of this file.

**Chunk 3** | source: `course_phys_130_workload.txt#0` | produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time,
not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because
you're learning the format.
```

Two paragraphs because the first is 95 characters, under my floor, so it
absorbed the next one. The weakest of the five: that second paragraph is
boilerplate that appears in nine workload files.

**Chunk 4** | source: `health_center.txt#1` | produced by: `chunker.py::split_documents`

```
The health centre

Counselling is separate, in the same building, and has its own intake process
with a shorter wait than people expect — usually three or four days for a first
session.
```

This is why I repeat the title. It's chunk 1, not chunk 0, so the title isn't
natively part of it. Without the repeat it reads "Counselling is separate, in
the same building" and never says which building.

**Chunk 5** | source: `housing_morrow_house_noise.txt#0` | produced by: `chunker.py::split_documents`

```
Noise levels in Morrow House

Asked about this a lot so writing it down. Loud until about 1am on weekends, no
enforced quiet hours.
```

Stands alone and names the building, which it has to: seven buildings have a
noise file and they differ only in the hours.

**What splitting cost me.** Promoting paragraphs to chunks also promoted the
boilerplate. The front loaded line is now its own chunk in five workload files,
and a line about the library being open until 2am is its own chunk in four.
They carry a title so they're distinguishable, but they say nothing specific
and there are nine of them competing for slots. Dropping any paragraph that
appears verbatim in three or more documents would fix it. I haven't done it.

## Sample Answer

**Question:** How much does a dryer cost in Morrow House?

**Answer:**

```
$ python app.py ask "How much does a dryer cost in Morrow House?"
  (best distance 0.304, cutoff 0.7)

A dryer in Morrow House costs $1.25.

Source: housing_morrow_house.txt (also found in housing_morrow_house_laundry.txt)

Sources retrieved: housing_morrow_house.txt, housing_morrow_house_laundry.txt
```

$1.25 is the only dry price in the corpus belonging to one building. The other
six charge $1.50 or $1.75, so an answer that drifted to a neighbour would show
up in the price itself.

Asked something the corpus doesn't cover:

```
$ python app.py ask "How do I write a for loop in Rust?"
  (best distance 0.877, cutoff 0.7)

I don't have enough information about that.
```

**My relevance cutoff:** 0.7, up from the 0.6 that shipped. Top k is 3, down
from 5.

| Question | In corpus? | Best distance |
|---|---|---|
| When are the walk in hours at the health centre? | yes | 0.133 |
| How many hours a week does BIOL 160 take? | yes | 0.294 |
| How much does a dryer cost in Morrow House? | yes | 0.304 |
| How late in the term can I drop a course? | yes | 0.304 |
| How many black and white pages does the printing quota cover? | yes | 0.322 |
| What is the capital of Mongolia? | no | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.848 |
| How do I write a for loop in Rust? | no | 0.877 |
| Who won the 1994 World Cup? | no | 0.886 |
| How do I change the oil in a diesel engine? | no | 0.934 |

The two groups are 0.133 to 0.322 and 0.825 to 0.934, so the gap is 0.322 to
0.825 and almost anything in it would score 10 out of 10 on these ten
questions.

I didn't take the middle, because that gap is flattered. I wrote those five
questions with the corpus open in another window. Rephrased the way someone
would actually type them, questions the corpus still answers score much worse:

| Loose phrasing | Best distance | Answer in corpus? |
|---|---|---|
| can I still get out of a class | 0.610 | yes, rank 2 |
| how bad is cell bio | 0.510 | yes, rank 1 |
| doctor | 0.815 | yes, rank 1 |

So the honest in corpus range runs to 0.610, not 0.322. At the 0.6 that
shipped, "can I still get out of a class" gets refused while the answer sits at
rank 2 in `admin_add_drop_deadline.txt`. That's the too low failure and the
default was one phrasing away from it. 0.7 clears every sentence shaped
question I can answer and still sits 0.125 under the nearest one I can't. I
didn't go higher because the one word query "doctor" hits 0.815, inside the out
of scope group, so past about 0.8 the two groups really do overlap.

**Why top k 3.** The answer chunk was rank 1 for all five questions, and the
distance jumps after rank 2 every time: 0.32 to 0.42 on Morrow House, 0.31 to
0.43 on BIOL 160, 0.38 to 0.49 on add/drop. Ranks 3 to 5 were the same
paragraph from the wrong course, matching because every workload file opens
"People keep asking so". Feeding the model three of those is how a wrong
citation happens, so I stopped at 3.

At top k 3 and cutoff 0.7: 5 of 5 test questions answered with the expected
fact retrieved, 5 of 5 out of scope questions refused.

**Grounding.** I left `GROUNDING_INSTRUCTION` alone, but tested it on four near
misses first, since the gate only catches the obvious ones. Asking the cost of
laundry in Tamsin Court is the one that convinced me: Tamsin has in unit
machines and no price, but Aldridge Hall at $1.75 and Fenwick Court at $2.00
were both in the same context window. It refused instead of borrowing one.

## How I Used AI

**1. The chunker merged paragraphs it should have left apart.** I asked Claude
to write `split_documents` from my notes: split on blank lines, 400 ceiling,
100 floor, repeat the title. What came back merged any two paragraphs whenever
they fit under the ceiling. My documents average 317 characters, so almost
everything merged straight back into one piece and only 5 of 88 documents split
at all, which is what the starter already did. I changed the condition to merge
only while a piece is under the 100 floor, and 41 documents split. That version
also added the title after checking the size, so 7 chunks came out over my own
ceiling.

**2. It accepted 0.6 because my questions were too easy.** I asked for the two
distance groups so I could place the cutoff. They came back clean, 0.133 to
0.322 against 0.825 to 0.934, with 0.6 sitting safely in the gap. But I wrote
those questions with the corpus open, so I asked it to rerun them phrased the
way a student would type them. "can I still get out of a class" scored 0.610
with the answer at rank 2, meaning 0.6 would refuse it. I set the cutoff to
0.7.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
