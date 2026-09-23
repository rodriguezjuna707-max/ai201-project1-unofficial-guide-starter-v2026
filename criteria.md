# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

Laundry comes up in 14 of my 88 files and the seven building laundry files are
near identical apart from the prices, so my Morrow House question has to beat
six lookalikes for a slot. The printing quota sits in one file and should be
easy. I left room for one miss because I expect Morrow House to be the failure.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

Every chunk already carries its filename, so naming a source is a formatting
job rather than a retrieval job. If it fails even once that is a bug in my
prompt and not a hard question, so there is no reason to accept four.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

Three of the five are from another planet and should sit far away, but two have
a neighbour in my corpus: the ibuprofen question sits near health_center.txt
and the Rust question sits near six CS course files. I expect one of those two
to land inside the cutoff and slip through.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

Taking every 9th chunk in index order (10 chunks out of roughly 88, and the
same 10 every time I check), at least 9 stand on their own: the chunk repeats
the subject from the title line of the file it came from, and neither end stops
in the middle of a sentence.

**Why this target:**

My files run 179 to 550 characters and none reach 800, so the starter chunker
never cuts anything and this passes for free today. It stops being free in
Milestone 3, because each file names its subject once in the title line and
never again, so a paragraph chunk from the middle of housing_old_brewhouse.txt
is about no building at all. I allow one miss because the exams files are under
210 characters and mostly title anyway.



---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

The cited source is the right one. For at least 4 of my 5 test questions, the
`expects` phrase I wrote for that question in `questions.py` appears in the
file the answer cites — not only in a sibling file about the same dorm or the
same course.

**Why this target:**

BIOL 160 has three files and 21 of my 88 are housing write ups, so at TOP_K 5
the whole sibling cluster comes back and citing the wrong twin is easy. I allow
one miss because I do not yet know whether the generator cites the file it
actually used.

I check against `expects` rather than against whatever the answer claimed,
because an answer can make several claims and I would pick a different one on a
different day.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
