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

This answers questions about student life at one university, from the
`campus_life` corpus: 88 short posts written the way students actually talk to
each other, covering dorms, dining halls, courses, and registrar policy. It
handles specific factual questions with one right answer, the kind you would
otherwise get by asking someone a year ahead of you. What does a dryer cost in
Morrow House, how late can you drop a course, how many hours a week is BIOL
160.

It retrieves the three closest chunks and answers only from those, naming the
file it used. If nothing in the corpus is close enough, it says it does not
have enough information instead of guessing. The corpus is deliberately full of
near duplicates, seven buildings with their own laundry file, three files per
course, so most of the work here is telling the right Morrow House from the
almost identical Aldridge Hall.

## Chunking Strategy

**Chunk size:** 450 characters maximum, 100 minimum, split on paragraph breaks
**Overlap:** none, replaced by repeating the document's title line in every chunk

I chose these before writing the function, from what `python app.py index`
reported about the corpus.

**I changed the ceiling once, from 400 to 450.** I picked 400 from the document
lengths, then measured the paragraphs and found the longest is 373 characters
and the longest title is 47. At 400 those two together would have forced a
paragraph apart, which is the one thing this chunker exists to prevent. 450 is
the smallest ceiling that never cuts anything in this corpus. The first version
also applied the ceiling before adding the title, so seven chunks came out over
my own stated limit; the check now covers the finished chunk.

**Why not 800.** The starter cuts at 800. My 88 documents run 178 to
549 characters, average 317, so the window is larger than my largest document
and the chunker never fired: 88 documents went in and 88 chunks came out. That
is not one thought per chunk, it is one file per chunk, and those are different
things here. `housing_old_brewhouse.txt` is 550 characters covering the
building's history, the heating, the laundry prices and the noise. Ask about
noise and the matching chunk is mostly about heating. A 400 cap is below every
multi topic document in the corpus, so it forces those apart, while still
sitting above the 178 to 250 range where the single topic files live so those
stay whole.

**Why split on paragraph breaks.** These documents already mark their own
divisions with blank lines, and the divisions are topical: one paragraph is the
heating, the next is the laundry. Cutting on a character count instead ignores
a boundary the writer already put there. The starter shows what that costs on
the other corpora, where it produced a 24 character chunk reading
`d Sundays and after 5pm.` on `city_guides` and a 2 character chunk reading
`t.` on `advice_threads`. Both are the tail of a document that did not divide
evenly, and neither can answer anything.

**Why a 100 character floor.** Paragraphs here run about 80 to 150 characters,
so splitting on every blank line alone would produce fragments. Anything under
100 in this corpus is a heading or a one line aside, so a chunk that short gets
merged into the paragraph after it rather than stored on its own.

**Why no overlap.** The starter carries 120 characters between neighbours. At a
400 cap that would duplicate almost a third of every chunk into the next one,
and this corpus already has near duplicate documents on purpose. Seven
buildings have a laundry file and they are identical apart from the prices, so
adding character overlap would manufacture more lookalikes in the one place
retrieval is already struggling. What the overlap was protecting against is a
fact getting separated from its context, and here that context is the subject
name. Every document names its subject once, in the title line, and never
again, so the body of `housing_old_brewhouse.txt` says "the heating is uneven"
without saying which building. Repeating the title line at the top of every
chunk from that file fixes the actual problem that overlap was aimed at, and
costs about 30 characters instead of 120.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

All five printed by `python app.py chunks -n 5`, which samples by stride across
the corpus. 135 chunks from 88 documents.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript. Nothing anywhere on the registrar's site says this plainly,
and students find out from each other.
```

Stands on its own. Both deadlines and the consequence of missing the first are
in the chunk, so "how late can I drop" is answerable from this alone.

**Chunk 2** — source: `course_cs_340.txt#0` — produced by: `chunker.py::split_documents`

```
CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus
a project that runs the whole term. Assessment: one midterm and a final, both
open-book. Lightly curved, usually two or three points.
```

Stands on its own, and the course code is in it, which matters because CS 340
has three files and CS 210 is a near twin of all three.

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time,
not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because
you're learning the format.
```

Two paragraphs, not one. The hours paragraph is 95 characters, under my 100
floor, so it absorbed the paragraph after it. This is the floor doing its job,
but it is also the weakest of the five: the second paragraph is boilerplate
that appears in nine workload files.

**Chunk 4** — source: `health_center.txt#1` — produced by: `chunker.py::split_documents`

```
The health centre

Counselling is separate, in the same building, and has its own intake process
with a shorter wait than people expect — usually three or four days for a first
session.
```

This is the one that shows why the title is repeated. It is chunk 1, not chunk
0, so the title line is not originally part of it. Without the repeat it reads
"Counselling is separate, in the same building" and never says which building,
which is the failure criterion 4 is looking for.

**Chunk 5** — source: `housing_morrow_house_noise.txt#0` — produced by: `chunker.py::split_documents`

```
Noise levels in Morrow House

Asked about this a lot so writing it down. Loud until about 1am on weekends, no
enforced quiet hours.
```

Stands on its own and names the building, which it has to: seven buildings have
a noise file and they differ only in the hours.

### What splitting cost me

Worth recording because it is a real downside of my change, not a bug. Cutting
these documents apart promoted boilerplate that used to be buried inside a
larger chunk. `It's front-loaded — the first month is heavier than the rest` is
now a chunk of its own in five different workload files, and a line about the
library being open until 2am is a chunk of its own in four. They pass the
stands-on-its-own test and they carry a title, so they are distinguishable, but
they say nothing specific and there are now nine of them competing for slots.
Under the starter's chunker they were harmless filler inside a chunk that also
held real content. Dropping a paragraph that appears verbatim in three or more
documents would fix it, and I have not done that yet.

## Retrieval and the Cutoff

**Top-k:** 3 (was 5) **Cutoff:** 0.7 (was 0.6)

Best distance for each question, measured against the 135 chunk index.

| my five test questions | best | out of scope | best |
|---|---|---|---|
| walk in hours at the health centre | 0.133 | capital of Mongolia | 0.825 |
| hours a week for BIOL 160 | 0.294 | ibuprofen dosage | 0.848 |
| dryer cost in Morrow House | 0.304 | Rust for loop | 0.877 |
| how late can I drop a course | 0.304 | 1994 World Cup | 0.886 |
| pages in the printing quota | 0.322 | diesel oil change | 0.934 |

**Why top-k 3.** The chunk holding the answer came back at rank 1 for all five
questions, and in every case the distance jumps after rank 2: 0.32 to 0.42 on
Morrow House, 0.31 to 0.43 on BIOL 160, 0.38 to 0.49 on add/drop. Ranks 1 and 2
are the right building or the right course. Ranks 3 to 5 were the same
paragraph from a different one, matching because every workload file opens with
"People keep asking so" and closes with the same front-loaded line. They are
not on topic, they share a sentence pattern. Handing three of those to the
model is how criterion 5 fails, so I stopped at 3.

**Why 0.7 and not the 0.6 that shipped.** The table above looks like a 0.50
wide gap with acres of room, and that reading is wrong. Those five questions
were written by someone with the corpus open. Typed the way a student actually
types, the same answerable questions score far worse:

| loose phrasing | best | answer is in the corpus? |
|---|---|---|
| is it expensive to dry clothes where I live | 0.455 | yes, rank 9 |
| how bad is cell bio | 0.510 | yes, rank 1 |
| can I still get out of a class | 0.610 | yes, rank 2 |
| doctor | 0.815 | yes, rank 1 |

So the honest in-corpus range runs to 0.610 for anything sentence shaped, not
0.322. At the shipped 0.6, "can I still get out of a class" is refused while
the answer sits in `admin_add_drop_deadline.txt` waiting at rank 2. That is the
too-low failure, and it was one phrasing away from happening by default.

0.7 clears every sentence shaped question I can answer and still sits 0.125
below the nearest thing I cannot. I did not go higher because the one word
query `doctor` reaches 0.815, which is inside the out of scope group at 0.825,
so above roughly 0.8 the two groups genuinely overlap and any cutoff up there
starts inventing answers.

At top-k 3 and cutoff 0.7: 5 of 5 test questions answered with the expected
fact in the retrieved chunks, 5 of 5 out of scope questions refused.

## Sample Answer

```
$ python app.py ask "How much does a dryer cost in Morrow House?"
  (best distance 0.304, cutoff 0.7)

A dryer in Morrow House costs $1.25.

Source: housing_morrow_house.txt (also found in housing_morrow_house_laundry.txt)

Sources retrieved: housing_morrow_house.txt, housing_morrow_house_laundry.txt
```

$1.25 is the right number and it is the one dry price in the corpus belonging
to a single building. Six other buildings charge $1.50 or $1.75, so an answer
that had drifted to a neighbour would be visible in the price itself.

And the same system asked something it has no documents for:

```
$ python app.py ask "How do I write a for loop in Rust?"
  (best distance 0.877, cutoff 0.7)

I don't have enough information about that.
```

### Is the grounding instruction strict enough?

I left `GROUNDING_INSTRUCTION` as it shipped, after testing rather than
assuming. The gate stops anything past 0.7, so what matters is the near misses:
questions that retrieve confident looking chunks which do not actually contain
the answer. I tried four.

| question | retrieved | answered |
|---|---|---|
| What time does the health centre close? | health_center.txt | refused, the file gives walk in hours only |
| How much does laundry cost in Tamsin Court? | tamsin_court, aldridge_hall, fenwick_court | refused |
| Does Morrow House have air conditioning? | housing_morrow_house.txt | refused |
| Is the workload in ENGL 205 heavier at the start? | three identical workload chunks | answered, cited ENGL 205 |

The Tamsin Court one is the result that decided it. Tamsin Court has in-unit
machines and no price, but Aldridge Hall at $1.75 and Fenwick Court at $2.00
were both sitting in the same context window. Borrowing one of those numbers is
the exact drift this layer exists to stop, and it did not happen.

The last row is criterion 5's hard case. The workload paragraph is word for
word identical across nine files, so all three retrieved chunks said the same
sentence and differed only in the title line my chunker prepends. It cited the
course that was asked about. That title repeat is now carrying weight in two
places, retrieval and attribution.

Tightening it further without having seen it drift would be guessing at a
problem I do not have evidence of. One cosmetic thing I would change if it
recurs: two of the refusals named a source while refusing, as in "I don't have
enough information ... (Source: health_center.txt)". Harmless, but it cites a
file that by definition did not answer anything.

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. The chunker merged paragraphs it should have left apart.** I asked Claude
to write `split_documents` from my notes: split on blank lines, 400 ceiling,
100 floor, repeat the title line. What came back merged any two paragraphs
whenever they fit under the ceiling. Since my documents average 317 characters
and the ceiling was 400, almost everything merged back into one piece and only
5 of 88 documents split at all, which is the same result as the starter. I
rewrote the condition to merge only while a piece is still under the 100 floor,
and 41 documents split. The same version also added the title after checking
the size, so 7 chunks came out over my stated ceiling.

**2. It accepted 0.6 because my own questions were too easy.** I asked for the
two distance groups so I could place the cutoff. They came back clean, 0.133 to
0.322 in corpus against 0.825 to 0.934 out, and the conclusion offered was that
0.6 sits safely in the gap. That gap is an artifact: I wrote those five
questions with the corpus open in another window. I asked it to rerun the same
questions phrased the way a student would type them. "can I still get out of a
class" scored 0.610 with the answer sitting at rank 2, so 0.6 would refuse a
question the corpus answers. I moved the cutoff to 0.7.

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
