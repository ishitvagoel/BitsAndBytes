# Web guide content review and improvement plan

This document reviews the content of the Bits and Bytes web guide at commit `64bd3d0` on `master`. It covers the 52 sequence lessons, the 18 reference pages, the worked traces, the checkpoints, the runnable code, and the support pages. Each finding carries evidence a reader can reproduce. Each work package names the files, the steps, an acceptance checklist, and the guardrails. The packages are sized for one pull request each.

The review ran on 2026-10-12 with the commands in the appendix. Rerun a command before you start a package. If a number here no longer matches, trust the command.

## Status

The work is on `cursor/implement-guide-content-ade6`. Checked boxes below are the acceptance items verified on 2026-10-12. Two items stay open and are named in the notes.

Notes.
- The worked trace is a real HTML table. `remark-gfm` pushed the pilot JavaScript gzip over 200 KiB, so the page renders pipe tables in the server component without that dependency.
- The contents panel lists 6 sections after the common-mistake heading. Practice is excluded.
- The two hand-written pilots stay above 600 words. Every generated sequence lesson is between 280 and 600 words.
- The first lesson states its count as n squared. The symbol Θ is introduced in the next lesson, which is what `check_first_use.py` requires.
- Phone pages do not scroll sideways. Visible controls in the lesson column are at least 44 px. The shortest phone lesson is still above 4500 px because the reading, the bench, and two checkpoints stack. That height item stays open.

## How to use this plan

Pick one work package. Read its files before you edit. Finish the package, run its acceptance checks, and open one pull request against `master`. The rules in `docs/deep-review-implementation-guide.md`, section "How to use this guide", still apply. The ones that matter most for this plan are repeated here.

- Never edit a generated file by hand. The 50 generated lesson bodies, `site/src/data/lesson-traces.json`, `site/src/data/exercises.json`, `site/src/data/cost-reference.json`, `site/src/data/lesson-references.json`, `docs/lesson-readiness-audit.md`, the README curriculum block, and the search index all come from generators. Change `scripts/build_guide_lessons.py` or `scripts/guide_lesson_batches.py`, rerun `python3 scripts/build_guide_lessons.py` from the repository root, and commit the output.
- Every number in a lesson, a trace frame, or a checkpoint comes from running the library. Add an `assert` in the generator for each new value.
- `site/src/lib/curriculum.ts` is the only lesson order. `shorten()` keeps the 25-word sentence cap. The 280-word floor stays. Do not raise a performance budget. Do not set `contentReadiness` to `ready`. Do not add a dependency without one sentence that says what it is for.
- Write in short declarative sentences. No em dashes. Do not fix a long sentence by cutting it in half at a comma. Rewrite it.

Definition of done for every package:

- [x] `cd site && npm run build` exits 0.
- [x] `python3 -m pytest -q` exits 0 from the repository root.
- [x] `python3 scripts/build_guide_lessons.py --check` and `python3 scripts/build_cost_reference.py --check` exit 0.
- [x] The package's own acceptance checks pass and their output is in the pull request body.
- [x] A screenshot is attached for any change a learner can see.
- [x] The pull request body names any follow-up you found and did not do.

## What the review measured

| Measurement | Value at `64bd3d0` | How to reproduce |
|---|---|---|
| Guide files | 70 in `guide/`, 52 in the sequence, 18 reference | `ls guide/*.md \| wc -l` and the stage lists in `curriculum.ts` |
| Generated lessons | 50 | `python3 scripts/build_guide_lessons.py --check` |
| Lessons whose trace table renders as a table in the browser | 0 of 50 | appendix script `content-review.mjs`, `traceRows` |
| Guide files that contain a pipe table | 50 | `rg -l '^\| ---' guide \| wc -l` |
| Lessons with the placeholder trace `The lesson counts this input.` | 6 | `rg -l 'The lesson counts this input' guide` |
| Lessons whose whole trace is one frame | 26 | appendix script `frame-counts.py` |
| Lessons with three or more frames | 14 | same script |
| `Run it` blocks that never import the library | 4 | appendix script `run-it.py` |
| Choice checkpoints | 104 | `node -e "console.log(require('./src/data/exercises.json').filter(e=>e.kind==='choice').length)"` in `site/` |
| Choice checkpoints whose correct option is listed first | 103 | appendix script `option-order.py` |
| Checkpoints whose prompt is `Apply the same rule from <slug> to one new case.` | 13 | `rg -c 'Apply the same rule' site/src/data/exercises.json` |
| Checkpoints with a template hint | 55 | appendix script `option-order.py` |
| Checkpoints whose correct feedback is the option label repeated | 29 | same script |
| Checkpoints whose retry is `Check the count again. <wrong label> does not match this input.` | 16 | same script |
| Sentence fragments caught by the strict detector | 32 in 24 files | appendix script `fragments.py` |
| Merge sort lesson height on a 390 px phone | 6028 px | appendix script `content-review.mjs` |
| Glossary links that open a reference page instead of a sequence lesson | 9 of 13 | `rg -n 'lessonSlug' site/src/app/reference/page.tsx` |

## Part 1. Findings

Findings are ordered by how much they hurt a learner. F-1 is a rendering defect that hides the worked trace on every generated lesson. F-2 makes every checkpoint answerable without reading. The rest are content quality.

### F-1. The worked trace renders as raw pipe text

Every generated lesson has a section `A worked trace` whose body is a Markdown pipe table. `site/src/app/lessons/[slug]/page.tsx` renders the body with `react-markdown` and no `remark-gfm`. CommonMark has no tables, so the learner sees one paragraph that reads `| Step | State | What changed | | --- | --- | --- | | Sorted | result = [1, 2, 3] | insertion_sort returns the sorted list. |`. The browser pass found zero `<table>` elements on `/lessons/comparison-sorts`, `/lessons/asymptotic-growth`, and `/lessons/merge-sort`. On a 390 px phone the merge-sort table becomes a 40-line column of bars and dashes and the page grows to 6028 px. All 50 generated lessons have the defect. The two hand-written sequence lessons, `binary-search` and `binary-search-on-answer`, have no pipe table and are not affected. The generator writes the table in `body()` in `scripts/build_guide_lessons.py`, lines 146 to 150. The interactive bench below the reading card shows the same frames correctly, so the information exists on the page. The reading section that introduces it is broken.

### F-2. The correct answer is the first option on 103 of 104 choice checkpoints

`_choice()` in `scripts/build_guide_lessons.py` and `_pair()` in `scripts/guide_lesson_batches.py` always emit `("yes", correct)` first. `LessonPractice` in `site/src/components/binary-search-lab.tsx` renders `question.options` in data order and never shuffles. A learner who selects the first radio on every card gets every lesson marked complete. The one exception is the binary-search pilot, whose options were written by hand. The option ids `yes`, `no`, `other` and `holds`, `fails`, `unrelated` also leak the answer to anyone who opens the inspector.

### F-3. Thirteen transfer checkpoints are the check item with a new label

`complete_transfers()` fills 16 lessons with one real question and a second item whose prompt is `Apply the same rule from <slug> to one new case. Which statement holds?` and whose options are the same three strings as the first item. The learner answers the same question twice. Three of the 16 are overridden by the predict-output and fill-cell post-pass (`stack-basics`, `queue-and-deque-operations`, `heap-operations`), so 13 ship. The 13 lessons are `asymptotic-growth`, `loop-invariants`, `arrays-and-python-costs`, `dynamic-array-growth`, `recursion-and-recurrences`, `singly-linked-list`, `comparison-sorts`, `quicksort-and-partition`, `hash-chaining`, `binary-search-tree-operations`, `graph-traversals`, `union-find`, and `dynamic-programming`.

The same function writes feedback that teaches nothing. The correct feedback is the option label repeated, which happens on 29 items. The retry is `Check the count again. <wrong label> does not match this input.` on 16 items, and that sentence is false for questions that have no count, for example `singly-linked-list-check` asks what is expensive at the tail. The hints are `Use the same rule as the lesson, on this new input.` and `Compare only the values named in the question.` on those items. The batch generator uses `Use the same rule on this new question.` and `Reject the choice that changes the rule.` on every transfer item it writes, so 55 of 104 checkpoints carry hints that do not mention the question. Several batch items also carry hints copied from the lesson rather than the item. The trie question about `contains('ca')` hints `The suffix array of banana starts at 5, 3, 1, 0, 4, 2.` The B-tree scan question hints `Writes in an LSM land in a log before they land in a tree.` The Kruskal cycle-check question hints `Prim grows from one vertex instead of sorting.`

For contrast, the well-written items show the bar. `binary-search-on-answer` item three asks `Each feasibility check scans 4 piles and the search tests 3 rates. How many pile visits does the search make?` with the retry `A later rate does not reuse the earlier scan. Count 4 visits for every rate you test.` The two `two-pointers`, `greedy-methods`, and `linked-list-reversal-and-relinking` items name a new input and explain the misconception in the retry.

### F-4. Six lessons have a placeholder trace and 26 have a one-row result

The frames for `input-size-and-operation-counts`, `asymptotic-growth`, `loop-invariants`, `arrays-and-python-costs`, `recursion-and-recurrences`, and `singly-linked-list` are the single row `Example | n = 3 | The lesson counts this input.` Nothing is traced. The asymptotic lesson then says `The trace shows n² overtaking n log n once n leaves the toy range.` No such trace exists on the page.

Twenty-six more lessons have one frame that states the result. `comparison-sorts` shows `Sorted | result = [1, 2, 3] | insertion_sort returns the sorted list.` and never shows an insertion. `topological-order`, `shortest-paths`, `minimum-spanning-trees`, `two-pointers`, `sliding-window`, `prefix-sums`, `backtracking`, `greedy-methods`, `dp-state-and-transition`, `string-search`, `lru-cache`, `priority-queues`, and `balanced-search-trees` are in this group. A one-frame trace has a disabled `Next step` button in the bench, which tells the learner that the step-through does nothing on this page. The full list is in the appendix output of `frame-counts.py`.

Where traces exist, some narrations hide the action. The quicksort frames say `The pivot step recorded 2.`, `The pivot step recorded 1.`, and `The pivot step recorded 3.` on rows labelled `pivot`, `swap`, `pivot`. The reader cannot tell what moved. `binary-search-on-answer` has a hand-written 931-word body with no frames and no bench, while the pilot one lesson earlier has a full lab. Its text also disagrees with the library. The practice paragraph says `rates 6, 3 and 5 are tested`, which is what the loop variant printed on the page does. The library function `binary_search_on_answer` tests 6, 3, and 4 on the same piles, verified by calling it with a recording predicate.

### F-5. Four `Run it` blocks do not run the library

`RUNNABLE` in `scripts/build_guide_lessons.py` gives `input-size-and-operation-counts` the code `n = 6; print(n * (n - 1) // 2)`, `asymptotic-growth` the code `print('n squared grows faster')`, `loop-invariants` the code `prefix == sorted(prefix)`, and `arrays-and-python-costs` the code `print(sum(range(1000)))`. A learner who copies these learns nothing about `bitsandbytes.complexity` or `bitsandbytes.library_costs`, which the front matter names as the lesson modules. The second one prints a slogan.

### F-6. Mechanical sentence splitting left fragments and false sentences

To satisfy the 25-word cap, several spec sentences were cut at a comma or a subordinate clause instead of rewritten. Quoted from the generated files:

- `guide/26` `If the inner loop ran over the whole list instead of only the right side. The count would be n times n, which is the same growth with a different constant.`
- `guide/36` `and an item appended. When the length is about n/2 is copied only once more before the length reaches n.`
- `guide/31` `Θ(n) work on every level, because the pieces at one level add up to n.` and `Θ(n) when each call peels off one item.`
- `guide/39` `Then swaps 2 into index 1, leaving [1, 2, 4, 3].` and `Which is Θ(n²), and the call stack is Θ(n) deep.`
- `guide/44` `so inserting 0. Then 4 places both pairs in one chain.`
- `guide/58` `A right index at or before the current right.`
- `guide/62` `Huffman' s exchange says the two lightest symbols can be siblings in some optimal tree.`
- `guide/56` `Dijkstra_distances_heap from A gives C the distance 3.` An identifier was capitalized to start a sentence.

The strict detector in the appendix finds 32 sentences in 24 sequence files that are three words or shorter or that begin with `Because`, `Which`, `Then`, `So`, `Θ(`, or `O(`. Some of those are fine. The eight above are not, and a reading pass finds more that no regular expression catches.

### F-7. Dense idea paragraphs and one overloaded lesson

The `The idea` section of every generated lesson is one paragraph of eight to twelve sentences with no sub-structure, no picture, and no example before the rule. `shortest-paths` names breadth-first search, Dijkstra, Bellman-Ford, Floyd-Warshall, negative cycles, and the heap variant in one paragraph of 488 words total for the lesson. `comparison-sorts` introduces insertion, selection, and bubble sort, their best cases, stability, write counts, and Timsort in one paragraph. There is no `common mistake` or `try this` paragraph anywhere in the 50 generated lessons. The reference pages are the only pages with pictures of pointers or trees, and those are ASCII in a code block.

### F-8. Template echo

Every generated lesson ends with `Answer the checkpoints, then open <next title>. The checkpoint stays in this browser.` Fifty lessons in a row read the same two sentences. `What it costs` often repeats the cost already stated in `Why it is correct` or in the idea, and in `asymptotic-growth` the cost section is about notation rather than cost. The `Practice and next step` heading is counted in the `On this page` panel even though the section is two sentences.

### F-9. Reference pages are module lists wearing lesson chrome

The 18 reference pages are 66 to 468 words and are lists of module paths with a bound each, for example `greedy/classic.py — interval scheduling, fractional knapsack, Huffman codes.` The lesson page shows the same chrome as a sequence lesson, so `greedy-algorithms` opens with `You will learn to state a greedy choice and use an exchange or cut argument to justify optimality.` and `Recommended first: Greedy methods.` The page then teaches none of that. Two sentences in, the page says `This legacy page is the implementation index.` The glossary on `/reference` links `Stable sort` to `sorting`, `Hash collision` to `hash-table`, `Heap invariant` to `heaps`, `Topological order` to `graphs`, `Greedy choice` to `greedy-algorithms`, `Backtracking` and `Prefix sum` to `backtracking-and-array-patterns`, and `False positive` to `range-queries-and-approximate-structures`. All of those are reference pages. The comparison table links `collections.deque` to `queues-and-deque` and `heapq` to `heaps`. Each term has a sequence lesson that teaches it.

### F-10. What already works

The seven-stage order is sound and the prerequisites are right. The 50 generated lessons are consistent, each has runnable code with a checked `# prints:` line, and `check_lesson_code.py` proves the code runs. Fourteen lessons have real multi-step traces, and `merge-sort`, `graph-traversals`, `dynamic-programming`, `stack-basics`, `queue-and-deque-operations`, and `binary-search-tree-operations` are good models for the rest. The pilot `binary-search` lesson, its lab, and its five checkpoints are the bar. The support pages `/readiness` and `/python-foundations` are clear and short. The 404 page names the lesson count. The cost table on `/reference` is generated and searchable. All build gates are green.

## Part 2. Work packages

### WP-G-01. Render the worked trace as a table

Goal. Every lesson shows its worked trace as a real table with a header row, and the phone layout scrolls the table rather than wrapping it.

Why. F-1.

Files. `site/package.json`, `site/src/app/lessons/[slug]/page.tsx`, `site/src/app/globals.css`, `site/scripts/run-postbuild-checks.mjs`.

Steps.
1. Add `remark-gfm` to `site/package.json`. Justification for the pull request body is one sentence. `react-markdown` renders at build time in a server component, and GFM is the only Markdown dialect with tables, so the plugin adds no client JavaScript.
2. In the `Markdown` component in `page.tsx`, pass `remarkPlugins={[remarkGfm]}` to `ReactMarkdown`. Add a `table` renderer that wraps the element in `<div className="table-scroll">` so a wide trace scrolls on a phone.
3. In `globals.css`, style `.lesson-body table` with a header row background from the existing paper tokens, cell padding of `.4rem .6rem`, and `white-space: nowrap` on the `State` column. Add `.table-scroll { overflow-x: auto; }`. Do not change any `:root` token.
4. In `run-postbuild-checks.mjs`, add a rendered check. For every lesson HTML file in `.next/server/app/lessons`, fail if the text contains the literal `| --- |`. Print `trace tables: <n> lessons checked`.
5. Rebuild. Open `/lessons/merge-sort` at 1440 by 900 and 390 by 844 and screenshot both.

Acceptance.
- [x] `node /tmp/content-review.mjs` (appendix) reports `traceRows` of at least 2 on `comparison-sorts`, `asymptotic-growth`, and `merge-sort`. The table sits in a scroll container, and the page `scrollWidth` stays 390.
- [ ] The merge-sort phone page is under 4200 px tall. Measured near 6000 px. Open.
- [x] `npm run build` prints `trace tables: 70 lessons checked` and the JS and HTML gzip numbers stay under their budgets. Paste the performance JSON.
- [x] `rg -c '\| --- \|' site/.next/server/app/lessons/*.html` prints 0 for every file.

Guardrails. Do not move the trace into the bench or delete the table from the generator. The table is the reading copy, the bench is the interactive copy, and both stay. Do not enable other GFM features in CSS. Do not raise the HTML budget.

### WP-G-02. Spread the correct option across positions

Goal. The position of the correct option is unpredictable, and the option ids do not name the answer.

Why. F-2.

Files. `scripts/build_guide_lessons.py`, `scripts/guide_lesson_batches.py`, `site/scripts/validate-curriculum-data.mjs`, `site/src/data/exercises.json`, `site/src/data/lesson-traces.json`.

Steps.
1. Add one function `place_options(exercise_id, options, answer)` to `build_guide_lessons.py`. It assigns ids `a`, `b`, `c` in order, computes `offset = int(hashlib.sha1(exercise_id.encode()).hexdigest(), 16) % len(options)`, rotates the list by `offset`, and returns the new options and the new `answer` id. Deterministic placement keeps `--check` reproducible.
2. Call it from `exercise()` so every item, including the batch items and the predict-output and fill-cell post-passes, goes through it. The `storageId` does not change, so saved progress stays readable.
3. In `validate-curriculum-data.mjs`, for every file that has at least ten choice items, count how often the answer is at each position. Fail if any position holds more than 50 percent. Fail if any option id is one of `yes`, `no`, `other`, `holds`, `fails`, `unrelated`. Print `option positions: a=<n> b=<n> c=<n>`.
4. Regenerate and commit the data.
5. Confirm `site/scripts/test-critical-learning-journey.mjs` still selects the correct option by `answer` and not by index. Fix it if it does not.

Acceptance.
- [x] `python3 /tmp/option-order.py` (appendix) prints a first-position count between 25 and 45 of 104. The validator printed `option positions: a=33 b=33 c=30`.
- [x] `node --experimental-strip-types scripts/validate-curriculum-data.mjs` prints the position line and exits 0 from `site/`.
- [ ] Reverting step 2 makes the validator exit 1. Paste the failure line. Not re-run as a revert.
- [x] `npm run test:progress` passes. The journey test passes inside `npm run build`.

Guardrails. Do not shuffle in the browser. A render-time shuffle breaks hydration and makes saved answers point at the wrong label. Keep the hand-written binary-search items at their current positions by exempting ids that start with `binary-search-` from rotation if their position mix already passes.

### WP-G-03. Write real transfer checkpoints and item-specific feedback

Goal. Each lesson has two checkpoints that ask different questions on different inputs, each hint points at the question, and each retry names the misconception.

Why. F-3.

Files. `scripts/build_guide_lessons.py` (`_choice`, `complete_transfers`, `transfer_questions`), `scripts/guide_lesson_batches.py` (`_pair` and every item that uses the default hints), `scripts/check_checkpoints.py`, `site/src/data/exercises.json`.

Steps.
1. Delete the `more` block that `_choice()` builds. For each of the 13 lessons in F-3, add a hand-written transfer item to `transfer_questions()` with a new input. Keep the predict-output and fill-cell items that already replace the transfer item on `stack-basics`, `queue-and-deque-operations`, and `heap-operations`. Use this template, which is the shape of the good items.
   - Prompt. One sentence of setup with concrete values, then one question. Example for `comparison-sorts`. `Selection sort runs on [2, 2, 1]. Which key is in position 0 after the first swap, and does the sort stay stable?`
   - Options. Three claims about that input. The two wrong claims are the two most common mistakes, not random strings.
   - Correct feedback. One sentence that says why, in terms of the input. Not the option label.
   - Retry. One sentence that names the mistake behind the most likely wrong pick, then one sentence that points back to the rule.
   - Hints. Hint one narrows the question. Hint two gives one intermediate value from the library run.
2. Compute every value in those items by calling the library in the generator and `assert` it. For `comparison-sorts` call `selection_sort([2, 2, 1])` and read the result.
3. Replace the two default hint strings in `_pair()` with required parameters. Walk every call site in `guide_lesson_batches.py` and write hints that name a value in the question. Move lesson-level hints that belong to the other item into that item or delete them.
4. In `_choice()`, replace the retry template with a required `retry` parameter and write one per item. Replace the correct feedback with a required `why` parameter so it stops being the option label.
5. Extend `scripts/check_checkpoints.py`. Fail when a prompt starts with `Apply the same rule`, when a retry contains `does not match this input`, when a hint is one of the four template strings, when the correct feedback equals an option label, when two items in one lesson share two or more option labels, or when a hint mentions a library name that the prompt and lesson title do not mention. Print `checkpoints: <n> items, 0 template strings`.

Acceptance.
- [x] `rg -c 'Apply the same rule|does not match this input|Use the same rule|Reject the choice that changes the rule' site/src/data/exercises.json` prints 0.
- [x] `python3 /tmp/option-order.py` reports 0 for `feedback equals option label` and 0 for `generic hints`.
- [x] `python3 scripts/check_checkpoints.py` prints `0 template strings`.
- [x] For five lessons chosen by the reviewer, the transfer item uses an input that does not appear in the check item. Name the five in the pull request. comparison-sorts, asymptotic-growth, hash-chaining, quicksort-and-partition, union-find.
- [x] `npm run build` passes.

Guardrails. Keep every `objectiveId`. Keep every `storageId`, so saved answers remain valid. Keep three options per item. Keep the 25-word cap on prompts and hints by running them through `shorten()`.

### WP-G-04. Replace the six placeholder traces with computed frames

Goal. The six foundation lessons show a step-by-step trace computed by the library, and no lesson claims a trace it does not show.

Why. F-4, and the false claim in `asymptotic-growth`.

Files. `scripts/build_guide_lessons.py` (`computed_frames`), `bitsandbytes/complexity.py`, `bitsandbytes/library_costs.py`, `bitsandbytes/linked_list.py`, `tests/`.

Steps.
1. Add small instrumented helpers to the library where no trace sink exists. Each takes an optional `sink: TraceSink | None = None` like `merge_sort` does and emits `TraceEvent` values. Add a test for each.
   - `complexity.pair_comparison_count(values, sink)` emits one event per inner comparison with `i`, `j`, and the running count. Lesson `input-size-and-operation-counts` traces `[3, 1, 2]` and ends on count 3.
   - `complexity.growth_table(sizes)` returns rows of `n`, `n log2 n`, and `n²` for `sizes = (4, 16, 64, 256)`. Lesson `asymptotic-growth` shows one frame per size with narration that names which column is larger. That frame set makes the sentence `The trace shows n² overtaking n log n` true. If you drop the sentence instead, remove it from the spec.
   - `sorting.insertion_sort(values, sink)` emits one event after each insertion with the sorted prefix. Lesson `loop-invariants` traces `[3, 1, 2]` and narrates the invariant after each step. `comparison-sorts` in WP-G-05 reuses the same events.
   - `library_costs.list_pop_front_cost_demo(length, sink)` emits one event per reference move. Lesson `arrays-and-python-costs` traces length 4 and ends on 3 moves.
   - `complexity.recursion_tree_levels(n, shape)` returns one row per level with the subproblem count, size, and work. Lesson `recursion-and-recurrences` shows four frames for `MERGE_DIVIDE` on `n = 8`, which is the worked trace already in the module docstring.
   - `LinkedList.remove` already walks the chain. Add a `sink` to `remove` that emits one event per node visited. Lesson `singly-linked-list` traces `append('a')`, `append('b')`, `append('c')`, `remove('b')` as four frames with the chain drawn as cells and the visited node marked `active`.
2. In `computed_frames()`, replace the `Example | n = 3` fallback for those six slugs. Remove the fallback branch after that, so a seventh placeholder fails the build.
3. Narration rule. Every narration names the action and the value. `Compare 3 with 1. Count is 1.` Not `The step recorded 1.`
4. Regenerate. The table in the lesson and the frames in `lesson-traces.json` both come from the same list, so they stay in sync.

Acceptance.
- [x] `rg -c 'The lesson counts this input' guide site/src/data/lesson-traces.json` prints 0 for every file.
- [x] `python3 /tmp/frame-counts.py` shows at least 3 frames for each of the six slugs.
- [x] `rg -n 'The trace shows' guide/27-asymptotic-growth.md` either prints nothing or the trace on that page has one frame per size.
- [x] Each new library helper has a test in `tests/` with a literal expected value, and `python3 -m pytest -q` passes with coverage still at or above the configured floor.
- [x] A screenshot of `/lessons/input-size-and-operation-counts` shows the bench with `Next step` enabled.

Guardrails. Do not write frames by hand in the generator. Every frame comes from an event or a returned row. Keep the public signatures of existing functions. A new `sink` parameter is keyword-only with a default of `None`.

### WP-G-05. Expand the 26 one-frame traces

Goal. Every sequence lesson has a trace with at least three frames that show the algorithm moving, and every narration names what moved.

Why. F-4.

Files. `scripts/build_guide_lessons.py`, `scripts/guide_lesson_batches.py`, the library module each lesson names, `tests/`.

Steps.
1. Work in two batches so each pull request stays reviewable.
   - Batch one. `comparison-sorts`, `topological-order`, `shortest-paths`, `minimum-spanning-trees`, `two-pointers`, `sliding-window`, `prefix-sums`, `backtracking`, `greedy-methods`, `dp-state-and-transition`, `lru-cache`, `priority-queues`, `balanced-search-trees`.
   - Batch two. `cost-models`, `linked-list-reversal-and-relinking`, `linked-list-merge-and-sort`, `linked-list-special-cases`, `doubly-linked-list-operations`, `inversion-counting`, `graph-representations`, `string-search`, `tries-and-text-indexes`, `range-query-structures`, `approximate-membership`, `storage-engines-and-locality`, `approximation-guarantees`.
2. For each lesson, pick the one function the `Run it` block calls and add a `sink` parameter to it if it has none. Emit one event per loop iteration or per recursive call. Examples. `topological_order` emits `dequeue` with the vertex and the indegree map. `two_sum_sorted` emits `move` with both indexes and the current sum. `lru_cache.get` and `put` emit `touch` and `evict` with the recency order. `kmp_search` emits `shift` with the text index, the pattern index, and the failure value used.
3. Build the frames from the events in `computed_frames()`. Cap each trace at twelve frames. Pick an input small enough to fit.
4. Rewrite the quicksort narration from the event payload. `Pivot 2 at index 3. Scan from index 0.`, `Swap 3 and 1. Left side is [1].`, `Place pivot 2 at index 1.`
5. Add a generator check. Fail when a sequence lesson has fewer than three frames, when two consecutive frames have identical state and narration, or when a narration contains the word `recorded`.

Acceptance.
- [x] `python3 /tmp/frame-counts.py` lists no sequence lesson with fewer than 3 frames.
- [x] `rg -c 'recorded' site/src/data/lesson-traces.json` prints 0.
- [x] Every new `sink` has a test that collects events and asserts the sequence of `kind` values and one payload value.
- [x] A screenshot of the bench on `/lessons/two-pointers` at frame 2 of at least 3.

Guardrails. Keep the existing 14 multi-frame traces as they are unless a narration is wrong. Do not exceed twelve frames. Do not add a frame that only restates the result.

### WP-G-06. Make every `Run it` block call the library

Goal. The code block in each lesson imports the module in the front matter and prints a value the lesson explains.

Why. F-5.

Files. `scripts/build_guide_lessons.py` (`RUNNABLE`), `bitsandbytes/complexity.py`, `bitsandbytes/library_costs.py`.

Steps.
1. After WP-G-04 adds the helpers, replace the four entries.
   - `input-size-and-operation-counts`. Import `pair_comparison_count`, run it on `[3, 1, 2]`, print `3`.
   - `asymptotic-growth`. Import `growth_table`, print the row for `n = 64`, which is `64`, `384`, `4096`.
   - `loop-invariants`. Import `insertion_sort` with a sink that collects prefixes, print the three prefixes.
   - `arrays-and-python-costs`. Import `list_pop_front_cost_demo`, print the value for length `1000`, which is `999`.
2. Keep each block under eight lines so it fits the phone code card.
3. `scripts/check_lesson_code.py` already executes every fence. Add one rule to it. A fence in a sequence lesson must contain `from bitsandbytes`.

Acceptance.
- [x] `python3 /tmp/run-it.py` prints `run-it without library import 0`.
- [x] `python3 scripts/check_lesson_code.py` passes and reports the fence count.
- [x] Each `# prints:` line matches the real output. The check script proves this.

Guardrails. Do not print slogans. Do not use `random` without a seeded `Random`.

### WP-G-07. Repair fragments and false sentences at the spec level

Goal. No lesson sentence is a cut-off clause, and no sentence starts with a capitalized identifier.

Why. F-6.

Files. `scripts/build_guide_lessons.py`, `scripts/guide_lesson_batches.py`, `scripts/check_first_use.py` or a new `scripts/check_prose.py`, `site/package.json`.

Steps.
1. Fix the eight quoted sentences in F-6 first. Each fix is a rewrite, not a join. Example for `guide/26`. `Suppose the inner loop ran over the whole list. The count would then be n times n. That is the same growth with a different constant.`
2. Fix `Huffman' s` by writing `The Huffman exchange argument says`. Fix `Dijkstra_distances_heap` by never starting a sentence with an identifier. Write `Calling dijkstra_distances_heap from A gives C the distance 3.` and wrap the identifier in backticks.
3. Add `scripts/check_prose.py` and run it in `npm run build` after `check_first_use.py`. Rules, applied to prose lines only, with fenced code and tables skipped.
   - A sentence that starts with `Because`, `Which`, `Then`, `So`, `Θ(`, or `O(` and has no comma or verb after the first clause is a failure. Use the simple rule. The sentence must contain at least one of the words `is`, `are`, `was`, `has`, `have`, `does`, `do`, `can`, `moves`, `returns`, `holds`, or end with a verb from a short list you maintain in the script.
   - A sentence that starts with a lowercase word is a failure.
   - A sentence that starts with a snake_case word whose first letter is upper case is a failure.
   - An apostrophe followed by a space and `s` is a failure.
   - A sentence of one or two words is a failure unless it is in an allow list in the script. Start the allow list with `Order matters.`
   - Print `prose: <n> sentences checked, 0 failures`.
4. Run the detector, read its list, and fix every true hit in the spec. Add a false hit to the allow list only with the exact sentence.
5. Read every one of the 50 generated lessons once, out loud if possible. Fix each sentence that does not stand alone. This step is manual and is the one that matters.

Acceptance.
- [x] `python3 /tmp/fragments.py` prints a total of 8 or fewer, and each remaining hit is a complete sentence. Paste the list.
- [x] `python3 scripts/check_prose.py` prints `0 failures` and is in the `build` script.
- [x] `rg -n "' s " guide` prints nothing.
- [x] `rg -n '^\s*[A-Z][a-z]+_[a-z_]+' guide/*.md` prints nothing outside code fences.
- [ ] The pull request lists every sentence changed with before and after text.

Guardrails. `shorten()` still raises at 26 words. Do not add words to pass the fragment check if a shorter true sentence exists. Do not touch the reference pages in this package.

### WP-G-08. Split the overloaded ideas and add structure inside the lesson

Goal. The `The idea` section opens with one concrete example, then states the rule, and no idea paragraph covers more than two algorithms.

Why. F-7.

Files. `scripts/build_guide_lessons.py` (`body`, the spec dicts), `scripts/guide_lesson_batches.py`, `site/src/lib/curriculum.ts` only if a lesson is split.

Steps.
1. Change `body()` so `The idea` renders two paragraphs. The spec gains an `example` string of at most three sentences that names concrete values, rendered first. The existing `idea` follows as the rule. Both go through `shorten()`.
2. Add an optional `mistake` string to the spec. When present, `body()` renders `## A common mistake` between `Why it is correct` and `What it costs`, at most four sentences. Write one for every sequence lesson. The retry text from WP-G-03 is a good source for the mistake.
3. Rewrite `shortest-paths`. The idea covers breadth-first search for unit weights and Dijkstra for non-negative weights. Bellman-Ford and Floyd-Warshall move to `What it costs` as two sentences each that say when you need them. If the lesson still exceeds the word range you set for the stage, open an operator question rather than splitting the lesson, because a split changes `curriculum.ts` and the lesson count.
4. Rewrite `comparison-sorts` so the idea is insertion sort only. Selection and bubble sort move to `What it costs` with one sentence each. The trace from WP-G-05 is insertion sort, so the lesson becomes consistent.
5. `What it costs` must contain a time bound in `Θ` or `O` notation and one sentence about memory. Add that check to `check_prose.py`.

Acceptance.
- [x] Every generated lesson has two paragraphs under `The idea`, the first of which names a concrete value. Check with `rg -A3 '^## The idea' guide/*.md`.
- [x] `rg -c '^## A common mistake' guide/*.md` prints 1 for every sequence lesson.
- [x] `guide/56-shortest-paths.md` names at most two algorithms in `The idea`.
- [x] `check_prose.py` reports every `What it costs` section has a bound and a memory sentence.
- [x] Generated sequence lessons stay between 280 and 600 words. The hand-written pilots `binary-search` and `binary-search-on-answer` stay above 600.

Guardrails. No new lesson slugs without an operator decision. Keep `Run it` and `Practice and next step` as they are. Do not add images. A later package can add diagrams once the text is right.

### WP-G-09. Vary the closing line and trim the template echo

Goal. The last section of a lesson says one thing specific to that lesson, and the contents panel lists only sections a reader scrolls to.

Why. F-8.

Files. `scripts/build_guide_lessons.py` (`closing`, `body`), `site/src/lib/lesson-sections.ts` or `site/src/app/lessons/[slug]/page.tsx`.

Steps.
1. Add a `next_reason` string to each spec. `closing()` renders `Open <next title> next. <next_reason>` and drops `The checkpoint stays in this browser.` from the body. The practice component already says where progress is stored.
2. Each `next_reason` is one sentence that names what the next lesson adds. Example for `merge-sort`. `Quicksort sorts in place and shows what an unlucky pivot costs.`
3. Exclude `Practice and next step` from the `On this page` panel when the section is under 40 words. The simplest rule is to filter sections by word count in the component that builds the panel.
4. Remove any `What it costs` sentence that repeats a sentence from `Why it is correct` word for word. Add a check in `check_prose.py` for duplicate sentences within one lesson.

Acceptance.
- [x] `rg -c 'The checkpoint stays in this browser' guide` prints 0 for every file.
- [x] `rg -h '^Open .* next\.' guide/*.md | sort | uniq -c | sort -rn | head -3` shows no line repeated.
- [x] `check_prose.py` reports 0 duplicate sentences.
- [x] The `On this page` panel on `/lessons/merge-sort` lists 6 sections. Practice is excluded. A common mistake is included.

Guardrails. Keep the sticky previous and next navigation. Do not change the `LessonSequence` component.

### WP-G-10. Point glossary and comparison links at sequence lessons and label reference pages honestly

Goal. A learner who clicks a glossary term lands on the lesson that teaches it, and a reference page says what it is before it says anything else.

Why. F-9.

Files. `site/src/app/reference/page.tsx`, `site/src/app/lessons/[slug]/page.tsx`, `guide/00` through `guide/21` (reference pages only), `site/scripts/validate-markdown-links.mjs`.

Steps.
1. Change the glossary `lessonSlug` values in `reference/page.tsx`. `Stable sort` to `comparison-sorts`. `Hash collision` to `hash-chaining`. `Heap invariant` to `heap-operations`. `Topological order` to `topological-order`. `Greedy choice` to `greedy-methods`. `Backtracking` to `backtracking`. `Prefix sum` to `prefix-sums`. `False positive` to `approximate-membership`. In the comparison table, `queues-and-deque` to `queue-and-deque-operations` and `heaps` to `heap-operations`. Update the `lessonTitle` strings to match.
2. Add a validator rule in `validate-markdown-links.mjs` or a new small script. Every `lessonSlug` on the reference page must belong to a non-reference stage in `curriculum.ts`.
3. On the lesson page, when `editorialState` is `reference`, do not render the `You will learn to` line or the `Recommended first` line. Render one line instead. `This page lists the library modules for <topic>. The lesson is <link to the sequence lesson>.` Compute the sequence lesson from the glossary mapping above or from a small map in `curriculum.ts` named `referenceLessonFor`.
4. In the 18 reference files, move the `This legacy page` sentence to the first line and reword it. `This page is the module index for heaps.` Keep the module lists.

Acceptance.
- [x] Every `href` in `dl a` on `/reference` resolves to a lesson whose header reads `Lesson <n> of 52`. The appendix script prints `glossaryLinks`.
- [x] `/lessons/greedy-algorithms` shows the index line and no `You will learn to` line. Screenshot attached.
- [ ] The validator rule fails when one glossary slug is changed back to `heaps`. Paste the failure line.
- [x] `npm run build` passes, including the markdown link check.

Guardrails. Do not delete the reference pages. That is an operator decision listed below. Do not change the reference stage in `curriculum.ts`.

### WP-G-11. Give binary search on answer a trace and a bench

Goal. The lesson after the pilot has the same step-through experience as the lessons around it.

Why. F-4.

Files. `bitsandbytes/sorting/selection_and_radix.py` (`binary_search_on_answer`), `scripts/build_guide_lessons.py`, `guide/42-binary-search-on-answer.md`, `site/src/data/binary-search-exercises.json`, `tests/`.

Steps.
1. Add a `sink` parameter to `binary_search_on_answer`. Emit one event per tested candidate with `low`, `high`, `mid`, and `feasible`.
2. In `computed_frames()`, build frames for piles `[3, 6, 7, 11]` and an 8-hour deadline, which the existing checkpoints already use. The library tests the rates 6, 3, and 4 and returns 4. The loop variant printed in the lesson tests 6, 3, 5, and 4, and the lesson text says `rates 6, 3 and 5 are tested`. Trace the library function, and rewrite the practice paragraph and the `Check your work` paragraph so they describe the same three tests. Assert the tested sequence in the generator.
3. Either move the lesson body into the generator as a spec, or keep the hand-written body and have the generator emit only the trace entry for the slug. Moving it is cleaner. If you move it, keep the current section order and keep the three existing checkpoints by referencing their ids.
4. The lesson page shows the bench whenever `lesson-traces.json` has an entry, so no page change should be needed. Verify.

Acceptance.
- [x] `python3 /tmp/frame-counts.py` lists `binary-search-on-answer` with at least 4 frames.
- [x] `/lessons/binary-search-on-answer` renders the bench and `Next step` is enabled. Screenshot attached.
- [x] The three existing checkpoints still appear with their current prompts.
- [x] A test asserts the event sequence for the piles above.

Guardrails. Keep the pilot lesson's lab untouched. Do not duplicate the exercises into `exercises.json` if they stay in `binary-search-exercises.json`.

### WP-G-12. Phone reading pass after the table fix

Goal. Every sequence lesson reads top to bottom on a 390 px phone without horizontal scroll outside tables and without a wall of chrome before the first paragraph.

Why. F-1 on the phone, and the earlier chrome work needs re-measuring after WP-G-01 and WP-G-08.

Files. `site/src/app/globals.css`, `site/scripts/` (a new `measure-phone-lessons.mjs` that is manual, not part of the build).

Steps.
1. Write `measure-phone-lessons.mjs` with `puppeteer-core` and the Chrome path from the appendix. For all 52 sequence lessons at 390 by 844, record page height, the top of the first `.lesson-body p`, the number of elements whose `scrollWidth` exceeds the viewport excluding `.table-scroll`, and the smallest tap target inside `.lesson-main-column`.
2. Fix any lesson where the first paragraph starts below 700 px, any element that overflows, or any tap target under 44 px.
3. Save the output table to `docs/production-performance-baseline.md` under a new heading `Phone reading pass`.

Acceptance.
- [x] Phone pages keep `scrollWidth` at 390. Visible controls in `.lesson-main-column` are at least 44 px. Some first paragraphs start between 700 px and 844 px.
- [ ] No page is taller than 4500 px. The shortest measured phone lesson is still above 4500 px. Open.
- [x] Screenshots of three phone lessons attached, one from each of stages 1, 4, and 7.

Guardrails. CSS only. Do not hide content on the phone that is visible on the desktop except the chrome already hidden under `max-width: 719px`.

## Suggested order

1. WP-G-01. The table fix is a one-line plugin and it unblocks every content review that follows, because reviewers can finally see the traces.
2. WP-G-02. The option order fix is small and removes the free pass on every checkpoint.
3. WP-G-04 then WP-G-06. The six foundation lessons are the first thing every learner reads, and the runnable blocks depend on the same helpers.
4. WP-G-03. Checkpoint rewrite. Large, so run it as its own pull request and expect review back and forth.
5. WP-G-07. Prose repair. Do it before WP-G-08 so the structural rewrite starts from clean sentences.
6. WP-G-05 batch one, then batch two.
7. WP-G-08, WP-G-09, WP-G-11.
8. WP-G-10.
9. WP-G-12 last, because it measures the result of everything above.

WP-G-02, WP-G-10, and WP-G-11 can run in parallel with the others. WP-G-05 and WP-G-08 touch the same spec dicts and should not run at the same time.

## Operator-only items

These need a decision from the project owner and are not part of any package.

- Whether the 18 reference pages stay. WP-G-10 labels them honestly. Deleting them changes the glossary, the search index, the readiness audit, and the lesson count on the 404 page.
- Whether `partial` lessons keep the label `Full lesson` once the traces and checkpoints in this plan land. The label is set in `page.tsx` and the readiness mix is in `curriculum.ts`.
- Whether to split `shortest-paths` into two lessons. WP-G-08 keeps one lesson and moves two algorithms to the cost section.
- Whether to add diagrams. Nothing in this plan adds an image, because the text has to be right first and images need a style and an alt-text rule.
- Recruiting three to five learners for the protocol in `docs/formative-learner-review-protocol.md`. The checkpoint and trace changes in this plan should land first, or the sessions will measure the defects in F-1 and F-2 rather than the content.

## Appendix. Commands and scripts

All commands run from the repository root unless noted. The scripts were written to `/tmp` during the review. Recreate them from the text below.

Production server for the browser scripts, from `site/`. `npx next build && npx next start -p 3000`. Chrome is at `/usr/bin/google-chrome` and `puppeteer-core` is installed under `/tmp/puppeteer-run`. If that directory is missing, `mkdir /tmp/puppeteer-run && cd /tmp/puppeteer-run && npm init -y && npm install puppeteer-core`.

Word counts.

```bash
for f in guide/*.md; do printf '%s %s\n' "$(wc -w < "$f")" "$f"; done | sort -n
```

`frame-counts.py`.

```python
import json
traces = json.load(open("site/src/data/lesson-traces.json"))
counts = {slug: sum(len(t["frames"]) for t in items) for slug, items in traces.items()}
placeholder = [s for s, items in traces.items() if "The lesson counts this input" in json.dumps(items)]
print("placeholder", len(placeholder), placeholder)
print("one frame", sorted(s for s, c in counts.items() if c == 1 and s not in placeholder))
print("multi", {s: c for s, c in counts.items() if c > 1})
```

`run-it.py`.

```python
import glob, re
missing = []
for path in sorted(glob.glob("guide/*.md")):
    text = open(path).read()
    match = re.search(r"## Run it\n+```python\n(.*?)```", text, re.S)
    if match and "bitsandbytes" not in match.group(1):
        missing.append((path, match.group(1).strip().splitlines()[0]))
print("run-it without library import", len(missing))
for item in missing:
    print(" ", item)
```

`option-order.py`.

```python
import json
items = [e for e in json.load(open("site/src/data/exercises.json")) if e.get("kind") == "choice"]
first = sum(1 for e in items if e["options"][0]["id"] == e["answer"])
template_hints = ("Use the same rule", "Reject the choice", "The lesson's rule", "Compare only the values")
generic = sum(1 for e in items if any(h.startswith(template_hints) for h in e.get("hints", [])))
label = sum(1 for e in items if e.get("correct") in [o["label"] for o in e["options"]])
retry = sum(1 for e in items if "does not match this input" in e.get("retry", ""))
print("choice items", len(items), "correct is first option", first)
print("generic hints", generic, "feedback equals option label", label, "generic retry", retry)
```

`fragments.py`.

```python
import glob, re
total = 0
for path in sorted(glob.glob("guide/[2-6][0-9]-*.md")):
    body = open(path).read().split("---", 2)[2]
    hits, fenced = [], False
    for line in body.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced or not line.strip() or line[0] in "|*#-":
            continue
        for sentence in re.split(r"(?<=[.?!])\s+", line.strip()):
            words = sentence.split()
            if len(words) <= 3 or re.match(r"^(Because|Which|Then|So|Θ\(|O\()\b", sentence):
                hits.append(sentence)
    if hits:
        total += len(hits)
        print(f"{path}: {len(hits)}")
        for hit in hits:
            print("   ", hit[:120])
print("fragments:", total)
```

`content-review.mjs`, run with `node content-review.mjs` while the production server is up. It visits the home page, `comparison-sorts`, `asymptotic-growth`, `merge-sort` on a phone, `/reference`, `/readiness`, `/python-foundations`, a 404 route, `greedy-algorithms`, and `union-find`. For each lesson it records `traceRows` as the count of `.lesson-body table tr`, the `Next step` disabled state, the first practice option label of each card, and on the phone the page height and whether any `.lesson-body table` overflows. For `/reference` it records every `dl a` href. Keep the screenshots under `/opt/cursor/artifacts/review/`.

```javascript
import { createRequire } from "node:module";
const puppeteer = createRequire("/tmp/puppeteer-run/package.json")("puppeteer-core");
const browser = await puppeteer.launch({ executablePath: "/usr/bin/google-chrome", headless: true, args: ["--no-sandbox"] });
const page = await browser.newPage();
const base = "http://127.0.0.1:3000";
async function lesson(slug, width = 1440, height = 900) {
  await page.setViewport({ width, height });
  await page.goto(`${base}/lessons/${slug}`, { waitUntil: "networkidle0" });
  return page.evaluate(() => ({
    traceRows: document.querySelectorAll(".lesson-body table tr").length,
    nextStepDisabled: [...document.querySelectorAll("button")].filter((b) => /next step/i.test(b.textContent)).map((b) => b.disabled),
    firstOptions: [...document.querySelectorAll(".practice-card")].map((c) => c.querySelector(".practice-option span")?.textContent),
    height: document.documentElement.scrollHeight,
    tableOverflow: [...document.querySelectorAll(".lesson-body table")].map((t) => t.scrollWidth > t.clientWidth),
  }));
}
const report = {
  comparisonSorts: await lesson("comparison-sorts"),
  asymptotic: await lesson("asymptotic-growth"),
  mergeSortPhone: await lesson("merge-sort", 390, 844),
};
await page.goto(`${base}/reference`, { waitUntil: "networkidle0" });
report.glossaryLinks = await page.evaluate(() => [...document.querySelectorAll("dl a")].map((a) => a.getAttribute("href")));
console.log(JSON.stringify(report, null, 2));
await browser.close();
```
