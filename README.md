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

The corpus is `campus_life`: 88 short posts about one university, covering
dorms, dining halls, courses, and registrar policy.

It answers specific questions that have one right answer. What a dryer costs in
Morrow House, how late you can drop a course, how many hours a week BIOL 160
takes. It pulls the three closest chunks, answers only from those, and names
the file. If nothing is close enough it says it doesn't have enough
information.

## Chunking Strategy

**Chunk size:** 450 characters max, 100 min, split on paragraph breaks
**Overlap:** none. I repeat the document's title line in every chunk instead.

**What I noticed.** `app.py index` showed the starter wasn't chunking anything:
88 documents in, 88 chunks out. My longest document is 549 characters and the
starter cuts at 800, so it never fired. But `housing_old_brewhouse.txt` is 550
characters covering the building's history, the heating, the laundry prices and
the noise. Ask about noise and the chunk is mostly about heating. One file was
not one thought, so I split on the blank lines the writers already put in. That
took 88 chunks to 135.

**Why 450.** The longest paragraph is 373 characters and the longest title is
47. I tried 400 first and those two together would have cut a paragraph in
half.

**Why 100.** Paragraphs run 80 to 150 characters. Anything under 100 here is a
heading or a one line aside, so it gets merged into the paragraph after it.

**Why no overlap.** Every document names its subject once, in the title line.
The body of `housing_old_brewhouse.txt` says "the heating is uneven" without
saying which building, and there are 21 housing files. Repeating the title
fixes that for 30 characters instead of 120.

## Sample Chunks

From `app.py chunks -n 5`. All five produced by `chunker.py::split_documents`.

**Chunk 1** | source: `admin_add_drop_deadline.txt#0` | produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript. Nothing anywhere on the registrar's site says this plainly,
and students find out from each other.
```

**Chunk 2** | source: `course_cs_340.txt#0` | produced by: `chunker.py::split_documents`

```
CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus
a project that runs the whole term. Assessment: one midterm and a final, both
open-book. Lightly curved, usually two or three points.
```

**Chunk 3** | source: `course_phys_130_workload.txt#0` | produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time,
not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because
you're learning the format.
```

Two paragraphs because the first is 95 characters, under my floor, so it
absorbed the next one.

**Chunk 4** | source: `health_center.txt#1` | produced by: `chunker.py::split_documents`

```
The health centre

Counselling is separate, in the same building, and has its own intake process
with a shorter wait than people expect — usually three or four days for a first
session.
```

This is why I repeat the title. It's chunk 1, not chunk 0, so without the
repeat it never says which building.

**Chunk 5** | source: `housing_morrow_house_noise.txt#0` | produced by: `chunker.py::split_documents`

```
Noise levels in Morrow House

Asked about this a lot so writing it down. Loud until about 1am on weekends, no
enforced quiet hours.
```

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

Off topic, for contrast:

```
$ python app.py ask "How do I write a for loop in Rust?"
  (best distance 0.877, cutoff 0.7)

I don't have enough information about that.
```

**My relevance cutoff:** 0.7, up from the 0.6 that shipped. Top k is 3, down
from 5.


| Question                                                      | In corpus? | Best distance |
| --------------------------------------------------------------- | ------------ | --------------- |
| When are the walk in hours at the health centre?              | yes        | 0.133         |
| How many hours a week does BIOL 160 take?                     | yes        | 0.294         |
| How much does a dryer cost in Morrow House?                   | yes        | 0.304         |
| How late in the term can I drop a course?                     | yes        | 0.304         |
| How many black and white pages does the printing quota cover? | yes        | 0.322         |
| What is the capital of Mongolia?                              | no         | 0.825         |
| What is the recommended dosage of ibuprofen for a headache?   | no         | 0.848         |
| How do I write a for loop in Rust?                            | no         | 0.877         |
| Who won the 1994 World Cup?                                   | no         | 0.886         |
| How do I change the oil in a diesel engine?                   | no         | 0.934         |

The gap is 0.322 to 0.825. I didn't take the middle, because I wrote those five
questions with the corpus open. Typed the way someone actually would, "can I
still get out of a class" scores 0.610 with the answer at rank 2, so 0.6 would
refuse a question the corpus answers. 0.7 clears that and still sits 0.125
under the nearest out of scope question.

Top k went to 3 because the answer was rank 1 for all five questions and the
distance jumps after rank 2 every time. Ranks 3 to 5 were the same paragraph
from the wrong course.

## How I Used AI

**1.** I asked Claude to write `split_documents` from my notes: split on blank
lines, 400 ceiling, 100 floor, repeat the title. It merged any two paragraphs
that fit under the ceiling, so with documents averaging 317 characters almost
everything merged back into one piece and only 5 of 88 split. I changed it to
merge only while a piece is under the 100 floor, and 41 split.

**2.** I asked for the two distance groups to place the cutoff. They came back
0.133 to 0.322 against 0.825 to 0.934, with 0.6 sitting fine in the gap. But I
wrote those questions with the corpus open, so I had it rerun them phrased
loosely. "can I still get out of a class" scored 0.610, which 0.6 would refuse.
I set the cutoff to 0.7.

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


| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| ---------------------------------------- | -------- | ------- | ------- | ------- | --------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

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
| --- | ----------- | --------- | --------------- |
| 1 |           |         |               |
| 2 |           |         |               |
| 3 |           |         |               |
| 4 |           |         |               |
| 5 |           |         |               |

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


| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| ---------------------------------------- | -------- | ------- | ------- | ------- | --------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

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
