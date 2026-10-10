# Binary-search formative learner review protocol

Use with 3–5 people who can read basic Python and have varied data-structures-and-algorithms confidence. The session is formative: look for where explanation and navigation fail, not whether the learner is capable. Do not record names or sensitive information. Ask permission before audio/video recording; written notes are enough.

## Preparation

- Use the same reachable preview build for every participant and note its commit/build date.
- Prepare a timer, a blank trace table, the question prompts below, and a neutral note sheet for participant ID, answer, confidence, hint used, confusion point and navigation issue.
- Do not teach binary search immediately before the session. Do not reveal a correct answer until the participant has finished the task.
- Ask the participant to think aloud. If they pause, say only: “What are you thinking about now?” Avoid hints that reveal the next step.

## Session flow (about 25 minutes)

### 1. Before the lesson (5 minutes)

Show this sorted input: `[2, 5, 9, 14, 18, 23, 31]`. Ask:

1. “Trace a search for 18. Which indexes or values would you inspect, in what order, and why?”
2. “Now search for 20. How will you know it is absent, and what interval remains at each step?”
3. “What must be true of the input for your method to work?”

Record the participant's own interval convention, boundary reasoning, stopping condition and confidence. Do not correct them yet.

### 2. Use the lesson (8 minutes)

Ask them to use the page as they normally would, while thinking aloud. Observe whether they:

- find purpose, prerequisites, section contents and the next action;
- predict a trace before using the interactive trace;
- understand interval boundaries, loop progress and duplicate behavior;
- use a hint, copy code, open source/tests, or navigate away to find missing context.

Record actions and questions verbatim when practical. Do not count time or scroll depth as learning evidence.

### 3. After the lesson (7 minutes)

Use a different input: `[1, 4, 8, 12, 16, 20, 24, 29]`.

1. “Trace a search for 15. Show every interval and say when the algorithm stops.”
2. “A teammate wrote `while left < right` but still updates `left = mid`. Find an input where it fails to make progress and explain a repair.”
3. “The value is found at index 3. What changes if the task is to insert it into a Python list, and what is the total cost?”

Ask the participant to explain why comparisons grow logarithmically, whether the input must be sorted, and why insertion may still take linear time.

### 4. Delayed retrieval (after several days)

Without reopening the lesson, send the same short follow-up to the participant through an agreed channel:

> On `[3, 6, 11, 17, 22, 28, 35, 41]`, trace the search for 30. Show the remaining range after each comparison and state the stopping condition. What precondition makes the reasoning valid?

Record correctness and explanation detail before offering feedback. Do not treat a missed response as proof the lesson failed.

## Evidence and revision

For each participant, note:

- correctness and reasoning quality for each pre-lesson, post-lesson and delayed task;
- whether they explain halving, boundary updates, termination and search-versus-insertion cost in their own words;
- each hint, repeated read, wrong turn, confusion point and navigation friction;
- what page or interaction likely caused the difficulty and a concrete revision to test.

After the first round, group repeated issues, revise the smallest relevant lesson or control, then repeat the affected tasks with learners who have not seen the revised wording. Keep time-to-completion secondary to explanation and transfer evidence.

## Response log

| Anonymous ID | Session date / build | Pre-lesson evidence | Post-lesson transfer | Hints / confusion / navigation | Delayed retrieval | Revision to test |
|---|---|---|---|---|---|---|
| Pending participant | — | — | — | — | — | Do not mark learner-review tasks complete without participant evidence. |

## Agent walkthrough, not a participant session

Recruiting 3–5 learners is still the operator's action. The row below is an automated browser session against the local production server. It does not replace the protocol above, and it must not be counted as participant evidence.

Build under test: working tree on `cursor/guide-learner-experience-ade6`, production server at `http://localhost:3000` after `npm run build`. Date: 2026-10-10. Lesson: Merge sort (`/lessons/merge-sort`), which is outside the binary-search pilot.

What the session did:

1. Home showed a Start here link to `/lessons/input-size-and-operation-counts`. Review queue and import/export controls were absent on a fresh visit.
2. Activating Start here opened Input size and operation counts.
3. Merge sort showed the header “Search and ordering · 19 of 52 · Next”, the badge “Full lesson”, and “About 7 min”.
4. Next step changed the narration from “The midpoint is 2. The halves are [3, 1] and [4, 2].” to “Each half of length 2 is sorted. The runs are [1, 3] and [2, 4].”
5. Choosing 2 and activating Check answer showed “Correct. The fronts are 3 and 2. The merge takes the smaller front, which is 2.”
6. Show hint revealed “A merge does not look past the front of either run.”
7. The previous-lesson title “Comparison sorts” computed to `rgb(36, 28, 20)` on a white card.
8. `/lessons/stacks` showed the badge “Reference” and the header “Python reference · Reference”. The page text did not include “of 52”.
9. At a 390px width, the sticky pager was visible. Its title color was `rgb(36, 28, 20)` on a white button. The bar behind it was `rgb(16, 19, 24)`.

| Anonymous ID | Session date / build | Pre-lesson evidence | Post-lesson transfer | Hints / confusion / navigation | Delayed retrieval | Revision to test |
|---|---|---|---|---|---|---|
| Agent session, not a person | 2026-10-10 local production build | Not collected. An agent cannot stand in for a pre-lesson trace. | Merge-sort Next step, Check answer, and Show hint matched the expected frame and the checkpoint for runs [1, 3] and [2, 4]. | Home Start here, reference labeling for stacks, and mobile title contrast all matched the checks above. | Not collected. | Keep human recruitment open. Do not close the learner-review task on this row. |
