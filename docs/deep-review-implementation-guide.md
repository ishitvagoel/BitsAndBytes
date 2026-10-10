# Deep review and implementation guide

This guide reviews the Bits and Bytes website, the lesson content, and the Python library at commit `5c0caf2` on `master`, and turns each finding into a work package that a coding model can finish in one pull request. Each package names the files, the steps, the acceptance checks, and the guardrails. Run the checks and paste their output into the pull request.

The review measured the repository on 2026-10-10 with the commands in the appendix. Rerun those commands before you start a package. If a number in this guide no longer matches, trust the command.

## How to use this guide

Pick one work package. Read its files before you edit anything. Finish the package, run its acceptance checks, and open one pull request against `master`. Do not combine packages in one pull request unless the guide says they depend on each other.

Rules that apply to every package:

- Branch from `origin/master` after `git fetch origin master`. Name the branch `cursor/<package-id>-<short-name>`.
- Keep the scope of the package. If you find a second problem, write it in the pull request body and leave the code alone.
- Do not raise a budget to make a check pass. The performance budgets live in `site/scripts/measure-static-performance.mjs` and the word floor lives in `scripts/build_guide_lessons.py`.
- Never edit a generated file by hand. The generated files are the 18 lesson bodies that `scripts/build_guide_lessons.py` lists, `site/src/data/lesson-traces.json`, `site/src/data/exercises.json`, `site/src/data/binary-search-traces.json`, `site/src/data/binary-search-source.json`, `site/src/data/lesson-references.json`, and `docs/lesson-readiness-audit.md`. Edit the generator and rerun it.
- Every number in a lesson, a trace frame, or a checkpoint must come from running the library. Add an `assert` in the generator for each new value.
- `site/src/lib/curriculum.ts` is the only list of stages, prerequisites, outcomes, and objective ids. Do not add a parallel outline in `README.md`, `CURRICULUM.md`, or `decisions.tsv`.
- An exercise must use an `objectiveId` that already exists in `curriculum.ts` for that lesson. The validator rejects anything else.
- Keep `bitsandbytes.learning-progress.v1` readable by the current `validateLearningProgress` in `site/src/lib/learning-progress.ts`. Add optional fields. Do not rename or remove fields.
- Do not set `contentReadiness` to `ready` on a lesson. That label is the pilot's bar, and only the operator moves a lesson there.
- Do not add a dependency to `site/package.json` or `pyproject.toml` without one sentence in the pull request that says what it is for.
- Write commit messages and pull request bodies as short declarative sentences. No em dashes.

Definition of done for every package:

- [ ] `cd site && npm run build` exits 0 and prints `contrast:`, `curriculum data:`, `markdown links:`, `critical learning journey:`, and the performance JSON.
- [ ] `python3 -m pytest -q` exits 0 from the repository root.
- [ ] `python3 guide/check_lessons.py` prints `check_lessons: ok`.
- [ ] `python3 scripts/build_guide_lessons.py --check` exits 0.
- [ ] The package's own acceptance checks pass and their output is in the pull request body.
- [ ] A screenshot is attached for any change a learner can see.
- [ ] The pull request body names any follow-up you found and did not do.

A brief for a coding model is the package section copied whole, plus one closing sentence. "Follow the rules in `docs/deep-review-implementation-guide.md`, section How to use this guide, and stop when the acceptance checklist is green." Commands in the acceptance lists run from the repository root unless the command starts with `cd site`. The `node scripts/...` commands run from `site/`.

## What the review measured

| Measurement | Value at `5c0caf2` | Command |
|---|---|---|
| Lesson files | 70 in `guide/` | `ls guide/*.md \| wc -l` |
| Lessons in the numbered sequence | 52 | the lesson header on any lesson page, or count non-reference entries in `curriculum.ts` |
| Readiness mix | 1 ready, 19 partial, 32 summary, 18 reference | `cd site && npm run report:readiness` |
| Lessons with a trace and a checkpoint | 19 (18 generated plus binary search) | `node -e "console.log(Object.keys(require('./site/src/data/lesson-traces.json')).length)"` in `site/` |
| Sequence lessons with neither a trace nor a checkpoint | 32 | the `summary` rows in `docs/lesson-readiness-audit.md` |
| Lesson bodies under 150 words | 17 in the sequence, 31 in total | the word-count loop in the appendix |
| Guide files with a code block | 2 of 70 | `rg -l '^```' guide \| wc -l` |
| Exercises | 25, all three-option multiple choice with two hints | `node -e "console.log(require('./site/src/data/exercises.json').length)"` in `site/` |
| Python test functions and collected tests | 135 functions, 238 collected, all pass | `rg -c "def test_" tests \| awk -F: '{s+=$2} END {print s}'` and `python3 -m pytest -q \| tail -1` |
| Library definitions and `Cost` docstrings | 390 functions and methods, 327 with a `Cost` heading, 60 with no docstring | the AST count in `scripts/check_cost_docstrings.py` after WP-L-02, or the `rg -c` commands in the appendix |
| Continuous integration | none, `.github/` does not exist | `ls -a .github` |
| Stylesheet | 2584 lines, 21 color tokens, 35 hex literals outside `:root` | `wc -l site/src/app/globals.css` |
| Production bundle for a lesson page, gzip | HTML 21.7 KiB, JS 191.1 KiB, CSS 7.3 KiB | `npm run build` in `site/`, performance JSON |
| Rendered text under 4.5:1 on cream | 25 nodes across 10 routes | the rendered audit described in the appendix |
| Home search for `big o` and `pop(0)` | 0 lessons found for each | type the terms into the home search |

## Part 1. Website UI and UX

### Findings

**F-UI-1. The header "Next" link shows a second logo mark.** `.site-header a::before` in `site/src/app/globals.css` draws the amber `B` badge on every anchor inside the header, and the lesson page portals a `Next` link into `#header-slot`. On every lesson the header reads `Foundations · 1 of 52 · [B] Next`. Measured on the desktop and the phone screenshot of `/lessons/input-size-and-operation-counts`.

**F-UI-2. Muted text on cream fails contrast outside the gated selectors.** `site/scripts/check-contrast.mjs` checks six selectors and six token pairs. A rendered audit of ten routes found 25 text nodes under 4.5:1. The color is `--muted` (`#b7b1a6`) on the cream `--surface` at 2.1:1 in `.support-lede`, `.readiness-intro`, `.reference-intro`, `.reference-source`, `.curriculum-result-count` on `/reference`, `.trace-state-table dt` in the binary-search lab, the note inside `.prerequisite-card`, and the paragraph on the not-found page. The amber `Question` eyebrow in `.readiness-question legend span` is 1.91:1 on cream. `.code-line-number` is 2.95:1 inside the dark code block.

**F-UI-3. Short lessons carry more chrome than content.** `/lessons/cost-models` has a 243-word body. Above the first paragraph the page stacks the kicker, the title, the summary, the badge, a `What you will learn` card, a `Recommended first` card, an `On this page · 3 sections` panel, and a `Modules 2` list. The first paragraph starts below the 900 px fold at 1440 px wide. The `Modules 2` heading is the module count rendered as part of the heading text. The kicker `Foundations · Lesson 3 of 52` repeats the header slot text one line below it.

**F-UI-4. The phone lessons menu is a flat list with no focus handling.** `site/src/components/lessons-menu.tsx` renders 52 links with the stage title repeated on every row. Opening the panel leaves focus on `body`. No link carries `aria-current`. The panel does not scroll to the current lesson. The only ways to close it are the scrim and Escape, and Escape unmounts the panel without returning focus to the button.

**F-UI-5. Desktop has no lesson list.** The **Lessons** button is `display: none` at 960 px and wider (`globals.css`, the `min-width: 960px` block). On a wide screen the header offers Home and Next and nothing else. Between 720 px and 959 px the learner has the menu button and the in-card previous and next links, but not the sticky pager.

**F-UI-6. Search covers metadata only.** `site/src/components/curriculum-index.tsx` matches the title, the summary, the outcomes, the stage title, and the prerequisite titles. `big o` and `pop(0)` return 0 lessons. `dijkstra` returns 1 because the shortest-paths summary names it. The reference page has 13 glossary terms and 5 tool rows, all hand-written in `site/src/components/reference-search.tsx`.

**F-UI-7. The learner never finishes anything.** No lesson has a done state. `bitsandbytes.learning-progress.v1` records visits and checkpoint attempts, but the home page shows `Visited` and `Last visited` and nothing else. A learner cannot see `3 of 7 done` for a stage or jump to the first unfinished lesson. The home resume line (`ResumeLine` in `site/src/components/resume-progress.tsx`) is plain text with no link. `ResumeCard`, which does link, is exported and never imported.

**F-UI-8. The home page is one 6210 px scroll on a phone.** All 70 rows render at once at 390 px wide. The desktop grid is two columns, the phone is one. There is no per-stage collapse and no `Continue` card.

**F-UI-9. The generic trace leaks enum words.** `site/src/components/trace-bench.tsx` prints `cell.status` under each cell, so a learner reads `idle`, `done`, `active`, and `excluded`. The binary-search lab prints `Possible` and `Ruled out`.

**F-UI-10. Export misses the generic traces, and the blocked-storage comment is wrong.** `local-progress-tools.tsx` exports and resets `bitsandbytes.binary-search-trace.v1` only. The 18 keys named `bitsandbytes.trace.<slug>.v1` stay behind. In `trace-bench.tsx`, the comment on the failed `setItem` says the trace still moves, but the snapshot is read back from `localStorage`, so a blocked write leaves the old step on screen.

**F-UI-11. Page metadata is shared.** `/`, `/reference`, and every lesson send the description `Lesson guide for the Bits and Bytes curriculum`. `/reference` and `/` share the title `Bits and Bytes`. Lessons set their own title in `generateMetadata` and not their description. Only `/readiness` and `/python-foundations` set both.

**F-UI-12. The build gate has gaps.** `npm run test:progress` is not part of `npm run build`. `site/scripts/run-postbuild-checks.mjs` exits 0 at once when `VERCEL=1`, so the production deploy never runs the rendered-link check, the journey test, or the gzip budget. `site/scripts/validate-curriculum-data.mjs` parses `curriculum.ts` with regular expressions, so a formatting change can fail the gate while TypeScript compiles.

**F-UI-13. Dead and duplicated code.** `getSourceExcerpt` in `site/src/lib/source-excerpts.ts` has no caller. `ResumeCard` has no caller. `site/src/data/lesson-slug-aliases.json` holds 70 identity pairs, so the redirect branch in the lesson page never fires. `.text-button`, the class on the hint button, has no CSS rule. `--paper` equals `--surface-soft` and `--amber` equals `--accent` in `:root`. Every lesson page passes the `progressConfigs` map for all 70 lessons into the client to record one objective. `useLocalJsonState` in `binary-search-lab.tsx` and the `useSyncExternalStore` blocks in five other components are two implementations of the same local-storage read.

**F-UI-14. What already works.** Focus outlines are visible on every tabbed element. The skip link is the first tab stop. Landmarks exist on every route. Every form control has a label. Trace cells carry a text state, not color alone. `prefers-reduced-motion` is honored. No tap target smaller than 44 px was found on the home page or the support pages. Every lesson page passes the critical journey test and the performance budget. `ready` and `partial` both read `Full lesson`, which is a deliberate learner-facing label. Part 2 moves the generated lessons toward the pilot's bar so that label stays honest.

### Work packages

#### WP-UI-01. Draw the logo mark only on the brand link

Goal. The header shows one `B` mark.

Why. F-UI-1.

Files. `site/src/app/layout.tsx`, `site/src/app/globals.css`.

Steps.
1. Give the brand link a class, `site-brand`, in `layout.tsx`.
2. Change `.site-header a::before` to `.site-brand::before` in `globals.css`. Keep the layout rules on `.site-header a`.
3. Rebuild and open any lesson.

Acceptance.
- [ ] On `/lessons/merge-sort`, `getComputedStyle(document.querySelector('#header-slot a'), '::before').content` is `none` or `""`.
- [ ] A screenshot of the header shows one amber mark.
- [ ] `npm run build` passes.

Guardrails. Do not move the header slot or the menu button.

#### WP-UI-02. Gate every cream surface for contrast and fix the failures

Goal. No rendered text on a cream surface is under 4.5:1, and the build fails if that returns.

Why. F-UI-2.

Files. `site/src/app/globals.css`, `site/scripts/check-contrast.mjs`, a new `site/scripts/audit-rendered-contrast.mjs`.

Steps.
1. In `globals.css`, set the color of each selector in F-UI-2 to `var(--ink-muted)` where it sits on cream. Set the `Question` eyebrow to `var(--link)`. Lighten `.code-line-number` until it reaches 4.5:1 on its code background.
2. Add a static rule to `check-contrast.mjs`. Any rule whose selector contains a paper container class (`.reading-card`, `.support-page`, `.reference-page`, `.not-found-page`, `.learning-lab`, `.trace-bench`, `.prerequisite-card`, `.lesson-page-outcomes`, `.contents-panel`, `.module-list`, `.trace-state-table`) and whose `color` resolves to `--muted` or `--foreground` is a failure. Add the selectors from F-UI-2 to `paperSubjects`.
3. Add `audit-rendered-contrast.mjs`. It launches Chrome through `puppeteer-core` when that package is installed, visits the ten routes in the appendix at 1440 by 900 and 390 by 844, and prints every text node under its WCAG threshold and every control under 44 px. It is a manual check, not part of `npm run build`, because the build must not depend on a browser.
4. Run the rendered audit and fix anything it still reports.

Acceptance.
- [ ] `node scripts/check-contrast.mjs` prints the selector count and the container rule count and exits 0.
- [ ] Reverting one of the F-UI-2 fixes makes `check-contrast.mjs` exit 1. Paste the failure line.
- [ ] The rendered audit prints `0` low-contrast nodes on all ten routes.
- [ ] CSS gzip stays under 10240 in the performance JSON.

Guardrails. Keep `--muted` for the dark shell. Do not darken the shell background.

#### WP-UI-03. Make the chrome fit the lesson length

Goal. The first paragraph of a short lesson is on the first screen, and no block repeats another.

Why. F-UI-3.

Files. `site/src/app/lessons/[slug]/page.tsx`, `site/src/components/module-list.tsx`, `site/src/lib/lesson-sections.ts`, `site/src/app/globals.css`, `site/scripts/test-critical-learning-journey.mjs`.

Steps.
1. Remove the `lesson-kicker` paragraph. The header slot already shows the stage and the position. Render the same text inside `<main>` only for users without JavaScript, with the `sr-only` class, because the header slot is a client portal and the server HTML has no position line.
2. Render `Recommended first` as one line under the badge, `Recommended first: Asymptotic growth`, with links. Delete the card and its note.
3. Render outcomes as one sentence, `You will learn to state assumptions behind a complexity claim and separate algorithm steps from container costs.`, when the lesson has 2 or fewer outcomes. Keep the card for 3 or 4. Keep `<details>` above 4.
4. Show `On this page` only when the markdown has 5 or more sections. The injected trace and practice sections do not count.
5. Move the module list into the `source-disclosure` block and change its heading to `Library code`. Render the count as a separate `<span>`, not inside the heading text.
6. Update the journey test if it asserts any removed text.

Acceptance.
- [ ] On `/lessons/cost-models` at 1440 by 900, `document.querySelector('.lesson-body p').getBoundingClientRect().top` is under 900.
- [ ] On `/lessons/binary-search` the outcomes card and the contents panel still render.
- [ ] `rg -n "lesson-kicker" site/src` returns nothing.
- [ ] `npm run build` passes, including the critical journey test.

Guardrails. Keep the sticky phone pager and the end-of-guide nav. Keep the `ResumeTracker`.

#### WP-UI-04. Group the lessons menu by stage, manage focus, and show it on desktop

Goal. Every learner can open a grouped lesson list from the header, land on the current stage, see the current lesson marked, and close the list from the keyboard.

Why. F-UI-4 and F-UI-5.

Files. `site/src/components/lessons-menu.tsx`, `site/src/app/layout.tsx`, `site/src/app/globals.css`.

Steps.
1. Read the current path with `usePathname()` and derive the current slug.
2. Group lessons by `stageTitle`. Render one `<h3>` per stage and the lessons under it. Drop the per-row stage span.
3. Set `aria-current="page"` on the current lesson link.
4. Add a `Close` button at the top of the panel. On open, move focus to it. On close, including Escape and the scrim, return focus to the **Lessons** button. Set `aria-modal="true"` and `role="dialog"` on the panel wrapper and trap Tab inside it while open.
5. On open, scroll the current link into view with `scrollIntoView({ block: "center" })`.
6. Remove the `display: none` on `.lessons-menu-button` at 960 px and wider. On wide screens open the panel as a right-side drawer of at most 24rem instead of a full-screen sheet.
7. Show the sticky pager up to 959 px instead of 719 px, so the 720 px to 959 px range has the same previous and next controls as a phone.

Acceptance.
- [ ] At 390 px and at 1280 px on `/lessons/merge-sort`, after clicking **Lessons**, `document.activeElement` is inside `#lessons-menu-panel`.
- [ ] `document.querySelector('#lessons-menu-panel [aria-current="page"]').getAttribute('href')` is `/lessons/merge-sort`.
- [ ] After Escape, `document.activeElement` is the **Lessons** button.
- [ ] The panel has 7 stage headings and 52 links.
- [ ] At 800 px wide, `.lesson-nav-sticky` has `display: grid`.
- [ ] `npm run build` passes and the JS gzip for a lesson page grows by less than 2 KiB.

Guardrails. Reference pages stay out of the menu.

#### WP-UI-05. Replace enum words in trace cells with learner words

Goal. A trace cell reads `comparing` or `ruled out`, never `idle`.

Why. F-UI-9.

Files. `site/src/components/trace-bench.tsx`, `scripts/build_guide_lessons.py`.

Steps.
1. Add a `Record<TraceCellStatus, string>` in `trace-bench.tsx` with `idle` as an empty string, `active` as `comparing`, `chosen` as `chosen`, `done` as `done`, and `excluded` as `ruled out`.
2. Allow a scenario to override the map with an optional `labels` object. Add that field to the `TraceScenario` type and to the generator's scenario dictionaries where a lesson needs its own words, for example `placed` for sorts and `visited` for graph traversal.
3. Render the mapped label and keep the status class for color.

Acceptance.
- [ ] On `/lessons/merge-sort`, no `.search-cell-state` text is one of `idle`, `active`, `done`, `excluded`, `chosen`.
- [ ] `python3 scripts/build_guide_lessons.py --check` exits 0 after you rerun the generator.
- [ ] `npm run build` passes.

Guardrails. Do not change the status ids. The stored trace state in local storage does not include labels.

#### WP-UI-06. Give a lesson a done state, link the saved place, and show stage progress

Goal. A learner sees `3 of 7 done` on each stage, the home page offers the first unfinished lesson, and the saved place is a link.

Why. F-UI-7.

Files. `site/src/lib/learning-progress.ts`, `site/src/components/resume-progress.tsx`, `site/src/components/binary-search-lab.tsx` (the `LessonPractice` component), `site/src/components/trace-bench.tsx`, `site/src/components/curriculum-index.tsx`, `site/src/components/local-progress-tools.tsx`, `site/src/app/page.tsx`, `site/scripts/test-learning-progress.mjs`.

Steps.
1. Add an optional `completedAt` ISO string to the per-lesson record in `learning-progress.ts`. `validateLearningProgress` must accept records without it.
2. Mark a lesson done when the learner answers every checkpoint on the page correctly. Lessons without checkpoints are done when the `ResumeTracker` section observer reaches the last section.
3. Add a `Mark as done` button at the end of the article for manual completion. It toggles `completedAt`.
4. Replace `ResumeLine` with the existing `ResumeCard` and link it to `/lessons/<slug>#<sectionId>`. Delete `ResumeLine`.
5. On the home page, show `n of m done` in each stage heading and a `Continue with <title>` card above the syllabus. The card links to the lesson that follows the most recently completed lesson in sequence order. If that lesson is also done, it links to the first lesson in sequence without `completedAt`. Hide the card when nothing is done.
6. Include `completedAt` in export and import.

Acceptance.
- [ ] `npm run test:progress` passes with a new case that round-trips `completedAt`.
- [ ] In a fresh browser, answer the merge-sort checkpoint correctly. The home page then shows `Continue with Quicksort and partition` and `Search and ordering · 1 of 8 done`.
- [ ] Keyboard activation of the saved-place link lands on the saved heading.
- [ ] Import of a progress file exported before this change still succeeds.
- [ ] Home JS gzip stays under 204800.

Guardrails. Local storage only. No account, no network.

#### WP-UI-07. Search the lesson bodies

Goal. `big o` finds Asymptotic growth and `pop(0)` finds Arrays and Python sequence costs.

Why. F-UI-6.

Files. A new `site/scripts/build-search-index.mjs`, `site/public/search-index.json`, `site/src/components/curriculum-index.tsx`, `site/package.json`. The index is generated. State in the pull request whether it is committed or ignored.

Steps.
1. Write the index builder. For each lesson, emit the slug, the title, every heading, every inline code token, and the body with markdown stripped and lower-cased. Run it before `next build` in the `build` script.
2. In `curriculum-index.tsx`, fetch `/search-index.json` the first time the query reaches 2 characters. Until it loads, keep the current metadata match.
3. Rank title matches above heading matches above body matches. Show the matched heading under the lesson title.
4. Change the result count so the live region is silent while the query is empty.

Acceptance.
- [ ] Typing `big o` on the home page lists Asymptotic growth first.
- [ ] Typing `pop(0)` lists Arrays and Python sequence costs.
- [ ] The performance JSON shows no change to the initial JS because the index loads on demand. State the index file size in the pull request.
- [ ] `npm run build` passes.

Guardrails. Reference pages may appear in results but after sequence lessons.

#### WP-UI-08. Set page metadata per route

Goal. Every route has its own title and description.

Why. F-UI-11.

Files. `site/src/app/page.tsx`, `site/src/app/reference/page.tsx`, `site/src/app/lessons/[slug]/page.tsx`, `site/src/app/layout.tsx`.

Steps.
1. Export `metadata` from `page.tsx` and `reference/page.tsx` with a title and a one-sentence description.
2. In `generateMetadata` for lessons, set `description` to `lesson.summary` and add `openGraph.title`.
3. Keep the layout defaults as the fallback.

Acceptance.
- [ ] `curl -s http://localhost:3000/reference | rg -o '<title>[^<]*'` prints `Glossary and library choices | Bits and Bytes`.
- [ ] `curl -s http://localhost:3000/lessons/merge-sort | rg -o 'name="description" content="[^"]*"'` prints the merge-sort summary.

Guardrails. None.

#### WP-UI-09. Shorten the phone home page

Goal. The home page at 390 px wide is under 3000 px tall with the current stage expanded.

Why. F-UI-8.

Files. `site/src/components/curriculum-index.tsx`, `site/src/app/globals.css`.

Steps.
1. Below 720 px, render each stage with its first four lessons and a `Show n more` button, the pattern that `site/src/components/module-list.tsx` already uses.
2. Expand the stage that contains the last visited lesson, and the first stage when nothing was visited.
3. Keep the search results unfiltered by the collapse. A search shows every match.

Acceptance.
- [ ] `document.documentElement.scrollHeight` on `/` at 390 by 844 is under 3000 with no visits in local storage.
- [ ] Searching `heap` shows every heap lesson even inside a collapsed stage.
- [ ] The desktop layout at 1440 px is unchanged. Attach before and after screenshots.

Guardrails. Do not hide the `Python reference` stage. Collapse it like the others.

#### WP-UI-10. One local-storage path and a complete export

Goal. Every component reads local storage through one hook, a blocked write still advances the trace, and export carries every trace.

Why. F-UI-10 and F-UI-13.

Files. A new `site/src/lib/use-local-json-state.ts`, `site/src/components/binary-search-lab.tsx`, `site/src/components/trace-bench.tsx`, `site/src/components/curriculum-index.tsx`, `site/src/components/review-queue.tsx`, `site/src/components/resume-progress.tsx`, `site/src/components/local-progress-tools.tsx`.

Steps.
1. Move `useLocalJsonState` out of `binary-search-lab.tsx` into `use-local-json-state.ts`. It keeps the in-memory copy when `setItem` throws and dispatches the `bitsandbytes:local-state:<key>` event.
2. Replace the `useSyncExternalStore` blocks in the other five components with that hook.
3. In `local-progress-tools.tsx`, export, import, and reset every key that starts with `bitsandbytes.trace.`. Keep the binary-search key.
4. Delete the comment in `trace-bench.tsx` that claims the trace moves when storage is blocked, because the hook now makes it true.

Acceptance.
- [ ] In a browser with `localStorage.setItem` overridden to throw, **Next step** on `/lessons/merge-sort` still changes the narration.
- [ ] An exported progress file after one step on merge sort contains `bitsandbytes.trace.merge-sort.v1`, and import restores that step in a fresh profile.
- [ ] `rg -n "useSyncExternalStore" site/src/components` returns nothing.
- [ ] `npm run test:progress` passes.

Guardrails. Do not change any storage key name.

#### WP-UI-11. Close the build-gate gaps and delete dead code

Goal. The build runs every check in every environment, and no unused export remains.

Why. F-UI-12 and F-UI-13.

Files. `site/package.json`, `site/scripts/run-postbuild-checks.mjs`, `site/scripts/validate-curriculum-data.mjs`, `site/src/lib/source-excerpts.ts`, `site/src/components/resume-progress.tsx`, `site/src/data/lesson-slug-aliases.json`, `site/src/app/lessons/[slug]/page.tsx`, `site/src/app/globals.css`.

Steps.
1. Add `npm run test:progress` to the `build` script before `next build`.
2. In `run-postbuild-checks.mjs`, replace the `VERCEL === "1"` early exit with a check that the `.next` output exists. If the checks cannot run on Vercel because the output layout differs, print the reason and still run the gzip budget on the files that are present.
3. In `validate-curriculum-data.mjs`, import `curriculum.ts` with `--experimental-strip-types`, as `generate-lesson-readiness-audit.mjs` already does, and drop the regular expressions.
4. Delete `getSourceExcerpt`, `ResumeCard` or `ResumeLine` (whichever WP-UI-06 did not keep), the alias file and its redirect branch, the `.page`, `.lede`, `.course-rail`, and `.course-place-chapters` rules, and the duplicate tokens `--paper` and `--accent` after replacing their uses.
5. Add a rule for `.text-button` with a 44 px minimum height.
6. Pass only the current lesson's `progressConfigs` entry to `LessonPractice` and `ResumeTracker`.

Acceptance.
- [ ] `VERCEL=1 npm run build` prints the journey and performance output instead of skipping.
- [ ] `rg -n "getSourceExcerpt|lesson-slug-aliases|ResumeLine" site/src site/scripts` returns nothing (or `ResumeCard`, if that is the one you removed).
- [ ] For each exported function and component in `site/src/lib` and `site/src/components`, `rg -n "<name>" site/src site/scripts` returns at least one line outside the defining file. List the names you checked.
- [ ] The lesson page HTML no longer contains the objective ids of other lessons. Check with `curl -s http://localhost:3000/lessons/merge-sort | rg -c "binary-search-prediction"` printing `0`.

Guardrails. Keep the four `!important` declarations in the reduced-motion block.

## Part 2. Learner content

### Findings

**F-C-1. A learner meets an empty lesson at step 3.** 32 of the 52 lessons in the numbered sequence are `summary` pages with no trace and no checkpoint. 17 of them are under 150 words, for example `guide/58-two-pointers.md` at 111 words. The third lesson, `cost-models`, is 243 words and shows `About 2 min`. The 18 generated lessons and the two binary-search lessons are the only pages with practice.

**F-C-2. The generated checkpoints repeat the trace.** In `scripts/build_guide_lessons.py` the merge-sort question asks which value is taken next, which is the next table row. The heap question asks for the root, which the table shows as `4`. The stack and queue questions ask for the second pop and the second dequeue, both printed. Each generated lesson has one exercise tied to one objective id, so the second objective (and two of the three for dynamic programming) has no exercise and never enters the review queue.

**F-C-3. Frames are hand-written and only the final value is asserted.** The generator asserts `merge_sort([3, 1, 4, 2]) == [1, 2, 3, 4]` and `fibonacci_modulo(6, 1000) == 8`, then emits frames it does not compute. The heap lesson shipped with a wrong intermediate array once and was fixed by hand. Quicksort's frames match `_partition` only when the pivot is already at the end, and the assert uses `Random(0)` and checks the sorted result only.

**F-C-4. Specific content errors.**
- The union-find option labelled `two-links` reads `2 to 0, two links if compression is off and 2's parent is 0`. A parent of 0 is one link, and the `correct` text says one hop. (`site/src/data/exercises.json`, the `union-find-check` item, written by the generator.)
- `curriculum.ts` says union-find teaches `union-by-size`. `bitsandbytes/union_find/disjoint_set.py` implements union-by-rank, and the lesson says rank.
- `curriculum.ts` says heap-operations teaches `sift-up`. The lesson shows only sift-down and heapify.
- `curriculum.ts` lists `traceIds: ["binary-search-core"]` for binary search. No file defines that id. The pilot's scenarios are `present`, `missing`, `single`, `empty`, and `duplicates` in `site/src/data/binary-search-traces.json`.
- `guide/42-binary-search-on-answer.md` prints a loop with `while low < high` and `high = middle`. The library's `binary_search_on_answer` in `bitsandbytes/sorting/selection_and_radix.py` keeps an `answer` variable and sets `high = middle - 1`. The lesson's third objective has no exercise.
- `guide/06-binary-search.md` says `about 15 minutes` in its text while the page computes 18.
- `guide/26-input-size-and-operation-counts.md` uses `Θ` and `O` with `prerequisites: []`. The next lesson defines them.
- `guide/58-two-pointers.md` uses `invariant` and `monotone` with only `arrays-and-python-costs` as a prerequisite. `loop-invariants` is lesson 4.
- `guide/44-hash-chaining.md` defines `load factor` in the sentence that uses it. `guide/49-heap-operations.md` says `complete tree` without defining it.

**F-C-5. Practice has one shape.** All 25 exercises are three-option multiple choice with two hints, a `correct` string, and a `retry` string. There is no predict-the-output, trace-completion, or code-reading item. The review queue (`site/src/components/review-queue.tsx`) shows the outcome sentence for a due objective, not a question. Intervals are 3 days after a correct answer, 7 after a correct review, and 1 after a retry (`site/src/lib/learning-progress.ts`).

**F-C-6. No lesson shows runnable code.** No guide file contains an `import` line. 68 of 70 have no code block. The generated lessons show trace tables and prose, and name the module only in front matter. The pilot is the only lesson with a source excerpt, and that excerpt comes from a build script.

**F-C-7. The reference pages still carry facts the sequence lacks.** The `Industry` paragraphs in `guide/04-stacks.md` (a Python `list` as a stack), `guide/05-sorting.md` (Timsort, stability, `O(n log n)`), and `guide/13-graphs.md` (sparse graphs, `deque`, `heapq`) appear nowhere in the sequence lessons. Kosaraju, Bellman-Ford, Prim, 0-1 BFS, Floyd-Warshall, and the bipartite test are named only on the graphs reference page. `min_stack`, `sort_stack`, and `largest_rectangle` costs are only on the stacks page.

**F-C-8. Four documents describe the curriculum and disagree.** `docs/release-evidence.md` says 66 summary, 2 partial, 1 ready, 1 reference. `curriculum.ts` says 32, 19, 1, 18. `CURRICULUM.md` orders analysis, linear structures, trees and heaps and hashing, sorting, union-find, graphs. `curriculum.ts` puts sorting before hashing and trees and puts union-find inside Graphs. `README.md` section 7 bundles `linear/dynamic_array.py` under queues while the site teaches dynamic arrays in Foundations. `decisions.tsv` has 22 rows for module chapters and no rows for the focused lessons.

**F-C-9. Prose patterns.** The generated idea and cost paragraphs contain sentences of 28 to 33 words (`guide/44-hash-chaining.md` line 24 is 33 words). All 18 generated lessons end with the same sentence. Eleven of the 18 have no extra cost paragraph and seven do.

### Work packages

#### WP-C-01. Fix the content errors and make the trace ids a validated reference

Goal. Every statement in F-C-4 is true, and the validator rejects a `traceIds` entry that no file defines.

Why. F-C-4.

Files. `scripts/build_guide_lessons.py` (the union-find spec), `site/src/lib/curriculum.ts`, `guide/06-binary-search.md`, `guide/42-binary-search-on-answer.md`, `site/scripts/validate-curriculum-data.mjs`.

Steps.
1. Rewrite the union-find option to `2 to 0, one link, because find(1) returned 0 before 2 was linked`. Keep the option id. Rerun the generator.
2. Change the union-find outcome to `Explain path compression and union-by-rank`. Change the heap outcome to `Trace sift-down and heap construction` or add a sift-up frame to the heap scenario. Pick one and say which in the pull request.
3. Change `traceIds` for `binary-search` to the five scenario ids from `binary-search-traces.json`.
4. In `validate-curriculum-data.mjs`, load `lesson-traces.json` and `binary-search-traces.json` and fail when a `traceIds` entry is in neither.
5. Replace the `about **15 minutes**` sentence in the pilot with a sentence that does not state a number. The page computes the minutes.
6. In `guide/42-binary-search-on-answer.md`, either print the library's loop or add one sentence that says the printed loop is a variant and the library keeps an `answer` variable. Add an exercise for `binary-search-answer-multiply-check-cost` in `site/src/data/binary-search-exercises.json`, add its id to `exerciseIds` for `binary-search-on-answer` in `curriculum.ts`, and rerun the generator so it reaches `exercises.json`. The validator requires the two lists to match exactly.

Acceptance.
- [ ] In `site/`, `node scripts/validate-curriculum-data.mjs` exits 0, and exits 1 after you change one `traceIds` entry to `nope`. Paste both lines.
- [ ] `python3 -c "import json; print([o['label'] for e in json.load(open('site/src/data/exercises.json')) if e['lessonSlug'] == 'union-find' for o in e['options']])"` prints no label containing `two links`.
- [ ] `rg -n "union-by-size|binary-search-core|15 minutes" site/src guide` returns nothing.
- [ ] Every objective id of `binary-search-on-answer` appears in `exercises.json`, and `npm run build` passes.

Guardrails. Do not change the option id `two-links` because saved practice state keys on it.

#### WP-C-02. Make every checkpoint a transfer question and cover every objective

Goal. No generated checkpoint can be answered by reading the table above it, and every objective id in a generated lesson has at least one exercise.

Why. F-C-2.

Files. `scripts/build_guide_lessons.py`, the 18 generated lesson bodies, `site/src/data/exercises.json`, a new `scripts/check_checkpoints.py`.

Steps.
1. For each of the 18 lessons, rewrite the question on a new input. For merge sort, ask which value leaves the runs `[2, 5]` and `[3, 4]` after `2` and `3` are out. For the heap, ask which index holds the larger child of index 1 in a 6-item array. For the stack, ask what `push 1, push 2, pop, push 3, pop, pop` returns. For the queue, ask the same with a deque that appends left once. Each `retry` string must name the concrete failure, as the pilot does.
2. Add a second exercise per lesson for the objective id that has none. Dynamic programming gets two.
3. Compute every answer in the generator with the library and `assert` it.
4. Write `scripts/check_checkpoints.py`. For each generated lesson it loads the scenario frames and the exercises and fails if the correct option's label equals any cell text or any `state` value in that lesson's frames, or if any objective id in `curriculum.ts` for that lesson has no exercise.
5. Add the script to the `build` chain in `site/package.json` after `build_guide_lessons.py --check`.

Acceptance.
- [ ] `python3 scripts/check_checkpoints.py` exits 0, and exits 1 when you point one correct label at a table cell. Paste both.
- [ ] `node -e` over `exercises.json` prints 2 exercises per generated lesson and 3 for dynamic programming.
- [ ] Every generated lesson body stays above 280 words.
- [ ] In the browser, the second checkpoint renders on `/lessons/merge-sort` and `Check answer` works for both.

Guardrails. Keep the first exercise's `storageId` so saved answers survive. New exercises get new ids.

#### WP-C-03. Compute the frames from the library

Goal. Every frame the learner steps through is produced by the library function the lesson names, and `--check` fails when a frame drifts.

Why. F-C-3. Depends on WP-L-06, which adds the trace hooks.

Files. `scripts/build_guide_lessons.py`, `site/src/data/lesson-traces.json`, the 18 lesson bodies.

Steps.
1. For each scenario, replace the hand-written `frames` list with a function that calls the library with a `trace_sink` and maps each emitted event to a frame (`label`, `narration`, `state`, `rows`). Narration text stays hand-written per event kind. Values come from the event.
2. Keep one `assert` per scenario on the final result, and add one `assert` on the frame count.
3. For quicksort, trace the library's partition on the input it chooses with `random.Random(0)`, and let the narration say which pivot it picked.
4. Regenerate and diff `lesson-traces.json`. Explain every changed value in the pull request.

Acceptance.
- [ ] `python3 scripts/build_guide_lessons.py --check` exits 0.
- [ ] Editing one number in a library function's loop (for example the midpoint rule in `merge_sort`) and rerunning `--check` exits 1. Revert the edit. Paste the failure.
- [ ] `rg -c 'cell\("' scripts/build_guide_lessons.py` prints 0, because no cell is written by hand. The `cell`, `row`, and `frame` helpers are called only by the functions that map trace events.

Guardrails. Do not change any library function's public behavior. A `trace_sink` of `None` must cost nothing.

#### WP-C-04. Show runnable code with its output in every generated lesson

Goal. Each generated lesson has one Python block a learner can paste, and the build runs it.

Why. F-C-6.

Files. `scripts/build_guide_lessons.py`, the 18 lesson bodies, a new `scripts/check_lesson_code.py`, `site/package.json`.

Steps.
1. In `body()`, add a section `Run it` with one fenced `python` block. The block imports the function from its `bitsandbytes` module, calls it on the lesson's input, and shows the result in a comment or a `print` line. Build the block from the same values the generator asserts.
2. Write `scripts/check_lesson_code.py`. It extracts every fenced `python` block from `guide/*.md`, runs it in a subprocess with the repository root on `PYTHONPATH`, and compares the stdout with the `# prints:` line in the block. It fails on any mismatch or exception.
3. Add the script to the `build` chain and to the CI workflow from WP-L-01.

Acceptance.
- [ ] `python3 scripts/check_lesson_code.py` prints `lesson code: 18 blocks ran` and exits 0.
- [ ] Changing one expected output line makes the script exit 1. Paste the failure.
- [ ] `rg -l '^```python' guide | wc -l` prints at least 19.

Guardrails. Use only the standard library and `bitsandbytes`. No network.

#### WP-C-05. Bring the summary lessons in the sequence up to the generated template

Goal. Every lesson in the numbered sequence has an idea, a worked trace, the invariant, a cost derivation, one runnable block, and two checkpoints.

Why. F-C-1.

Files. `scripts/build_guide_lessons.py`, the summary lesson bodies, `site/src/lib/curriculum.ts`, `site/src/data/lesson-traces.json`, `site/src/data/exercises.json`.

Steps. Work in batches of four to six lessons per pull request, in sequence order, so the learner's path fills from the front:
1. Batch A. `cost-models`, `fast-slow-pointer-patterns`, `linked-list-reversal-and-relinking`, `linked-list-merge-and-sort`, `linked-list-special-cases`, `doubly-linked-list-operations`.
2. Batch B. `monotonic-stack-patterns`, `stack-parsing-and-expressions`, `noncomparison-sorts`, `order-statistic-selection`, `inversion-counting`.
3. Batch C. `hash-linear-probing`, `lru-cache`, `tree-traversals`, `balanced-search-trees`, `priority-queues`.
4. Batch D. `graph-representations`, `topological-order`, `shortest-paths`, `minimum-spanning-trees`.
5. Batch E. `two-pointers`, `sliding-window`, `prefix-sums`, `backtracking`, `greedy-methods`, `dp-state-and-transition`.
6. Batch F. `string-search`, `tries-and-text-indexes`, `range-query-structures`, `approximate-membership`, `storage-engines-and-locality`, `approximation-guarantees`.

For each lesson, add a spec to the generator with the same shape the 18 use, compute every value from the library, and set `contentReadiness: "partial"`. Keep the hand-written content that the generator does not replace by moving any unique sentence into the spec.

Acceptance per batch.
- [ ] Each lesson body is above 280 words and has the sections `The idea`, `A worked trace`, `Why it is correct`, `What it costs`, `Run it`, and `Practice and next step`.
- [ ] `scripts/check_checkpoints.py` and `scripts/check_lesson_code.py` pass.
- [ ] `npm run report:readiness` shows the batch's lessons as `partial` and the `summary` count drops by the batch size.
- [ ] The home page shows `Full lesson` and a word-derived minute count for each lesson in the batch.

Guardrails. One batch per pull request. Do not touch lessons outside the batch.

#### WP-C-06. Define each term where the sequence first uses it

Goal. A learner never meets `Θ`, `O`, `invariant`, `amortized`, `stable`, `load factor`, or `complete tree` before a lesson defines it or lists the defining lesson as a prerequisite.

Why. F-C-4, the last four bullets.

Files. `scripts/build_guide_lessons.py`, `site/src/lib/curriculum.ts`, `guide/58-two-pointers.md`, a new `scripts/check_first_use.py`.

Steps.
1. Write `scripts/check_first_use.py`. It takes a table of term to defining slug (`Θ` and `O` to `asymptotic-growth`, `invariant` to `loop-invariants`, `amortized` to `dynamic-array-growth`, `stable` to `comparison-sorts`, `load factor` to `hash-chaining`, `complete tree` to `heap-operations`), walks the sequence in `curriculum.ts` order, and fails when a lesson uses a term before its defining lesson unless the lesson is the defining one or lists it as a prerequisite.
2. Fix each failure. For `input-size-and-operation-counts`, write the count as `n(n - 1) / 2` and say `grows like n squared` instead of `Θ(n²)`. Add `loop-invariants` to the prerequisites of `two-pointers`. Define `load factor` and `complete tree` in their own sentence before use.
3. Add the script to the `build` chain.

Acceptance.
- [ ] `python3 scripts/check_first_use.py` exits 0 and prints the table it checked.
- [ ] Adding `amortized` to the body of `input-size-and-operation-counts` in a scratch copy makes it exit 1.

Guardrails. Do not reorder stages to make the check pass. Change the prose or the prerequisites.

#### WP-C-07. Move the industry facts into the sequence

Goal. Every fact listed in F-C-7 appears in a sequence lesson, so a reference page can be deleted without losing it.

Why. F-C-7.

Files. `scripts/build_guide_lessons.py` for generated targets, `guide/*.md` for hand-written targets, `guide/04-stacks.md`, `guide/05-sorting.md`, `guide/13-graphs.md`.

Steps.
1. Timsort, stability, and `O(n log n)` go into `comparison-sorts`. `heapq` goes into `heap-operations`. The Python `list` as a stack goes into `stack-basics`. `min_stack`, `sort_stack`, and `largest_rectangle` costs go into `monotonic-stack-patterns`. Sparse graphs with `deque` go into `graph-representations`. Kosaraju, Bellman-Ford, Prim, 0-1 BFS, Floyd-Warshall, and the bipartite test go into `shortest-paths` or `minimum-spanning-trees` as a short list of what the library has and where.
2. Leave the reference pages in place. Deleting them is the operator's call.

Acceptance.
- [ ] `rg -n "Timsort" guide/37-comparison-sorts.md`, `rg -n "heapq" guide/49-heap-operations.md`, `rg -n "Bellman" guide/56-shortest-paths.md`, and `rg -n "largest_rectangle" guide/33-monotonic-stack-patterns.md` each return a line.
- [ ] `python3 scripts/build_guide_lessons.py --check` exits 0.

Guardrails. One paragraph per fact. Do not copy the module lists.

#### WP-C-08. One source of truth for the curriculum documents

Goal. `README.md`, `CURRICULUM.md`, and `docs/release-evidence.md` either come from `curriculum.ts` or say in their first paragraph that they are a module map and not the lesson order.

Why. F-C-8.

Files. `site/scripts/generate-lesson-readiness-audit.mjs`, `README.md`, `CURRICULUM.md`, `docs/release-evidence.md`, `decisions.tsv`, `site/package.json`.

Steps.
1. Extend the audit generator to also write a stage-by-stage lesson list into `README.md` between `<!-- curriculum:start -->` and `<!-- curriculum:end -->` markers, and to accept `--check`, which exits 1 when the committed text differs.
2. Add `--check` to the `build` chain.
3. Add one sentence to the top of `CURRICULUM.md` and `decisions.tsv`'s header row that says they list modules, and that `site/src/lib/curriculum.ts` is the lesson order.
4. Replace the counts in `docs/release-evidence.md` with a link to `docs/lesson-readiness-audit.md`.

Acceptance.
- [ ] `node --experimental-strip-types scripts/generate-lesson-readiness-audit.mjs --check` exits 0, and exits 1 after you edit one lesson title inside the README markers.
- [ ] `rg -n "66 summary" docs` returns nothing.

Guardrails. Do not move module bullets out of the README.

#### WP-C-09. Add two practice kinds and show a question in the review queue

Goal. A learner meets predict-the-output and fill-the-cell items, and a due review shows a question.

Why. F-C-5. Depends on WP-C-02.

Files. `site/src/data/exercises.json` and its generator, `site/src/components/binary-search-lab.tsx` (`LessonPractice`), `site/src/components/review-queue.tsx`, `site/scripts/validate-curriculum-data.mjs`, `site/src/lib/learning-progress.ts`.

Steps.
1. Add a `kind` field to every exercise with the values `choice`, `predict-output`, and `fill-cell`. Existing items get `choice`.
2. `predict-output` carries a `code` string and options that are outputs. `fill-cell` carries a `frameLabel`, a `rowLabel`, a `cellIndex`, and options that are cell values.
3. In `LessonPractice`, render by `kind` with a `switch` whose `default` assigns to `never`.
4. In the validator, reject unknown kinds and reject a `fill-cell` whose frame or cell does not exist in the lesson's scenario.
5. In the review queue, show the prompt of the first exercise for the due objective and link to it with `#practice-section`.
6. Add at least one non-`choice` item to five generated lessons through the generator.

Acceptance.
- [ ] `node scripts/validate-curriculum-data.mjs` exits 1 for `kind: "essay"` and for a `fill-cell` with `cellIndex: 99`. Paste both.
- [ ] Five lessons render a non-choice item in the browser and `Check answer` grades it.
- [ ] After a wrong answer, the next day's review queue (simulate by editing `nextReviewAt` in local storage) shows the exercise prompt, not the outcome sentence.

Guardrails. Schema version stays 1. Old saved practice state must still validate.

#### WP-C-10. Keep generated sentences short and end each lesson with its own next step

Goal. No generated sentence is longer than 25 words, and the closing sentence of each lesson names the next lesson.

Why. F-C-9.

Files. `scripts/build_guide_lessons.py`, the 18 generated lesson bodies.

Steps.
1. Add a check inside the generator that splits each generated paragraph into sentences on `. `, `? `, and `! ` and raises `SystemExit` when a sentence has more than 25 words. Code spans count as one word.
2. Rewrite the sentences the check reports. Split the 33-word hash-chaining equality sentence and the 32-word priority-queue sentence into two each.
3. Read the next lesson for each generated slug from `curriculum.ts` order inside the generator, and end the body with `Answer the checkpoints, then open <next title>.` The last lesson in a stage names the first lesson of the next stage.
4. Regenerate.

Acceptance.
- [ ] `python3 scripts/build_guide_lessons.py --check` exits 0, and exits 1 with the offending sentence printed after you add a 30-word sentence to one spec in a scratch copy.
- [ ] `rg -c "then use Next for the following lesson" guide` prints 0.
- [ ] `rg -l "then open Quicksort and partition" guide` prints `guide/38-merge-sort.md`.

Guardrails. The 280-word floor stays. Split sentences, do not delete content.

## Part 3. Python library

### Findings

**F-L-1. The import path is uneven.** `bitsandbytes/__init__.py` exports seven names. `from bitsandbytes import DynamicArray` fails. `approximate`, `limits`, `range_queries`, `storage`, and `strings` have no `__init__.py`, so they import as namespace packages with no `__all__`. `hash_tables/__init__.py` omits `LinearProbingHashTable`, `sorting/__init__.py` omits `selection_and_radix`, `union_find/__init__.py` omits `Percolation`, `trees/__init__.py` omits `traversals`, and `graphs/__init__.py` omits `algorithms`. `tools/__init__.py` exports nothing.

**F-L-2. Containers disagree on errors, returns, and protocols.** An empty pop raises `StackEmptyError` on the stacks, `IndexError` on queues, the deque, the dynamic array, the doubly linked list, and the priority queue, and `RuntimeError` on `ReviewersList` (`bitsandbytes/linked_lists/reviewers.py`). A full stack raises `StackFullError` and a full circular queue raises `IndexError`. Trees use `insert` and `delete` returning `bool`. Lists use `remove` returning `None` and raising `ValueError`. Hash tables use `__delitem__` and `KeyError`. `Stack.push` returns the item, `MinStack.push` returns `None`, `PriorityQueue.push` returns an integer token. No class defines `__contains__`. `__eq__` exists only on `LinkedList`. `BinarySearchTree`, `Graph`, `Trie`, `BTree`, `SkipList`, and `BloomFilter` have no `__len__`.

**F-L-3. Cost docstrings are mostly present and sometimes wrong.** 327 of 390 functions and methods have a `Cost` heading. 60 have no docstring. 17 public ones have a docstring without `Cost`, including `binary_search_trace`, `dijkstra_distances_heap`, `SkipList.contains`, and `BTree.search`, `insert`, `put`, and `maybe_contains`. Wrong statements against the code:
- `linear/dynamic_array.py` `total_copy_cost_for_appends` says `O(log append_count)` while the body loops `range(append_count)`.
- `dynamic_programming/classic.py` `fibonacci_modulo` says `O(n)` extra memory for the table while the code keeps two integers.
- `trees/bst.py` `insert` says the call stack is `O(h)` for the recursive walk while the body is a `while True` loop.
- `library_costs.py` `insert_into_sorted` claims `O(n)` extra memory for a shift that moves references inside one list.
- `graphs/adjacency_list.py` `dijkstra_distances` says `O(V²)` in the summary and `O(V² + E)` in the Cost block.

**F-L-4. Tests pass and some cannot fail.** 135 test functions, 238 collected cases, all green. Fourteen assertions would pass with a broken implementation. `tests/test_analysis_writeups.py` pins docstring sentences, `tests/test_quicksort_expectation.py` pins two paragraphs of a module docstring, `tests/test_stack_aggregate.py` pins a `push` docstring sentence, `tests/test_heaps.py` checks only `values[0] == max(values)`, `tests/test_curriculum_completion.py` checks `len(permutations([1, 2, 3])) == 6` and `len(cover) >= 1` and `set(codes) == {"a", "b", "c"}`, `tests/test_union_find.py` checks `connected(0, 2)` without the representative, and `tests/test_binary_search_trace_fixtures.py` compares the trace to `binary_search` from the same file and the JSON fixture to the generator that wrote it. No test names `connected_components`, `prim_minimum_spanning_weight`, `longest_common_subsequence`, `sliding_window_maximum`, `suffix_array_with_lcp`, `backtrack_find`, `dag_dp_longest_path`, `lis_length_quadratic`, `max_non_adjacent_sum`, `unbounded_knapsack_max_value`, `map_inorder`, `WriteAheadLog`, `sequential_scan_sum`, `locality_scan_benchmark`, or `AlgorithmStack`.

**F-L-5. No tooling gate.** `pyproject.toml` is 14 lines. There is no `[build-system]`, so `pip install .` has no backend. There is no ruff, mypy, pyright, coverage, hypothesis, `py.typed`, pre-commit, or `.github/workflows`. The Python tests run only when someone runs them.

**F-L-6. Typing stops short of the comparisons.** `TypeVar` and `Generic[` appear 132 times in the library, but `T` is unbounded where the body uses `<` (`trees/bst.py`). There is no `Protocol` for comparable keys. `slots=True` is on the node dataclasses and not on the containers. No module uses PEP 695 syntax, `typing.Self`, or `match`.

**F-L-7. Duplicates and loose ends.** `stacks/stack.py` `Stack` is bounded with a default limit of 10 and `stacks/algorithm_stack.py` `AlgorithmStack` is unbounded. `MinStack` and `next_greater` use `AlgorithmStack`. `dijkstra_distances` (array scan, `graphs/adjacency_list.py`) and `dijkstra_distances_heap` (`graphs/algorithms.py`) are two Dijkstras and only the scan is exported. `ReviewersList` is a third list type with its own node. `approximate/structures.py` `PersistentStackFrame.pop` has `assert self.previous is not None or True`, which cannot fail. `heaps/priority_queue.py` `decrease_key` says the new priority must be strictly smaller and returns on an equal one. `# TRACE:` hooks exist only in `search/binary_search.py`.

### Work packages

#### WP-L-01. Add the maintainer gate

Goal. Every push runs the Python tests, a linter, a type checker, the lesson checks, and the site build.

Why. F-L-5.

Files. `pyproject.toml`, a new `.github/workflows/ci.yml`, a new `bitsandbytes/py.typed`.

Steps.
1. Add `[build-system]` with `hatchling` (or `setuptools`) and `[tool.ruff]` with `target-version = "py312"`, `line-length = 100`, and the rule sets `E`, `F`, `I`, `UP`, `B`.
2. Add `[tool.mypy]` with `python_version = "3.12"`, `strict = true`, and `files = ["bitsandbytes"]`. If strict mode reports more than you can fix in this package, list the failing modules under `[[tool.mypy.overrides]]` with `ignore_errors = true` and record the count in the pull request. Later packages remove entries from that list and never add to it.
3. Add `pytest-cov` to the `dev` extra and `--cov=bitsandbytes --cov-report=term-missing` to `addopts`.
4. Write `ci.yml` with two jobs. `python` runs `pip install -e .[dev] ruff mypy`, `ruff check .`, `mypy`, `pytest`, `python3 guide/check_lessons.py`, and `python3 scripts/build_guide_lessons.py --check`. `site` runs `npm ci` and `npm run build` in `site/` with Node 22.
5. Fix every ruff finding or add a per-rule ignore with a one-line reason.

Acceptance.
- [ ] `ruff check .` and `mypy` exit 0 locally. Paste the mypy summary line.
- [ ] `pytest` prints the coverage table. Record the total percentage in the pull request.
- [ ] The workflow runs green on the pull request. Link the run.
- [ ] `pip install -e .` succeeds in a fresh virtual environment.

Guardrails. Do not change library behavior in this package. Formatting and import order only.

#### WP-L-02. Make every Cost docstring true and checked

Goal. Every public function and method has a `Cost` block, the five wrong ones are fixed, and a script fails when a block is missing.

Why. F-L-3.

Files. The five modules in F-L-3, `search/binary_search.py`, `graphs/algorithms.py`, `approximate/structures.py`, `storage/engines.py`, a new `scripts/check_cost_docstrings.py`, `.github/workflows/ci.yml`.

Steps.
1. Fix the five statements listed in F-L-3 so they describe the code.
2. Add `Cost` blocks to the 17 public definitions that lack one. Use the same shape as `search/binary_search.py`, which names the input size variable, the loop or recursion count, and the extra memory.
3. Write `scripts/check_cost_docstrings.py`. It walks the AST of every module, fails for a public function or method with no `Cost` heading, and fails when a docstring contains `recurs` while the function body has no call to its own name.
4. Add the script to the CI `python` job.

Acceptance.
- [ ] `python3 scripts/check_cost_docstrings.py` prints `cost docstrings: 0 missing` and exits 0.
- [ ] Deleting the `Cost` block from one function makes it exit 1. Paste the line.
- [ ] `rg -n "O\(log append_count\)" bitsandbytes` and `rg -n "for the table" bitsandbytes/dynamic_programming/classic.py` return nothing.

Guardrails. Docstrings only. No logic changes.

#### WP-L-03. Export what the lessons name

Goal. Every package has `__init__.py` with `__all__`, every public class in a package is in that `__all__`, and the root exports the containers the lessons use. `guide/check_lessons.py` already imports every `module:` path, so this package does not repeat that check.

Why. F-L-1.

Files. `bitsandbytes/__init__.py`, the five missing `__init__.py` files, `hash_tables/__init__.py`, `sorting/__init__.py`, `union_find/__init__.py`, `trees/__init__.py`, `graphs/__init__.py`, `tools/__init__.py`, a new `scripts/check_exports.py`.

Steps.
1. Add `__init__.py` with `__all__` to `approximate`, `limits`, `range_queries`, `storage`, and `strings`.
2. Add the missing names to the package `__all__` lists.
3. Add `DynamicArray`, `LinkedQueue`, `LinkedDeque`, `ChainingHashTable`, `LinearProbingHashTable`, `BinarySearchTree`, `PriorityQueue`, `Graph`, and `DisjointSet` to the root `__all__`.
4. Write `scripts/check_exports.py`. It imports every name in every package `__all__`, and it fails when a public class (a CapWords name without a leading underscore) defined in a submodule is missing from that package's `__all__`. Node and frame helper classes go in an allowlist inside the script with one comment line that says why. The root package is exempt from the class rule and checked only for the names in step 3.
5. Add the script to CI.

Acceptance.
- [ ] `python3 scripts/check_exports.py` prints the package count and the class count and exits 0.
- [ ] Removing one name from a package `__all__` makes it exit 1. Paste the line.
- [ ] `python3 -c "from bitsandbytes import DynamicArray, DisjointSet"` exits 0.
- [ ] `find bitsandbytes -type d -not -name __pycache__ ! -exec test -e '{}/__init__.py' ';' -print` prints nothing.

Guardrails. Do not rename any module.

#### WP-L-04. One container protocol

Goal. Every container supports `len`, iteration, `in`, and `repr`, and an empty removal raises `IndexError` everywhere.

Why. F-L-2.

Files. `linked_list.py`, `doubly_linked_list.py`, `linear/dynamic_array.py`, `stacks/*.py`, `queues/*.py`, `deques/*.py`, `trees/bst.py`, `trees/llrb.py`, `hash_tables/*.py`, `heaps/priority_queue.py`, `linked_lists/reviewers.py`, a new `tests/test_container_protocol.py`.

Steps.
1. Make `StackEmptyError` subclass `IndexError` and `StackFullError` subclass `OverflowError`. Existing `except StackEmptyError` code keeps working.
2. Change `ReviewersList`'s empty removal to raise `IndexError`.
3. Add `__len__`, `__iter__`, `__contains__`, and `__repr__` where missing. `__repr__` shows the class name and the items in iteration order, for example `Stack([1, 2, 3])`.
4. Write `tests/test_container_protocol.py`, parametrized over one small instance of each container. For each it asserts the literal `len`, the literal list from iteration, `in` for a present and an absent item, the `repr` string, and that the empty removal raises `IndexError`.
5. Update the Cost blocks for any new method.

Acceptance.
- [ ] `pytest tests/test_container_protocol.py -q` passes with one parameter set per container, at least 12 sets.
- [ ] `python3 -c "from bitsandbytes import Stack, StackEmptyError; print(repr(Stack(limit=2))); print(issubclass(StackEmptyError, IndexError))"` prints `Stack([])` and `True`.
- [ ] `python3 scripts/check_cost_docstrings.py` still exits 0.

Guardrails. Do not change the return type of `push`, `enqueue`, or `insert` in this package. Note the inconsistency in the pull request for the operator.

#### WP-L-05. Replace the weak tests and cover the untested functions

Goal. Every test asserts a literal result of calling the code, and every public function listed in F-L-4 has one.

Why. F-L-4.

Files. The test files named in F-L-4, new tests for the listed functions.

Steps.
1. Delete each docstring-pin test or replace it with a call and a literal result. For `test_quicksort_expectation.py`, assert `quick_sort([3, 1, 4, 2], rng=random.Random(0)) == [1, 2, 3, 4]` and the comparison count the docstring promises for one input, if the function exposes it.
2. Rewrite `tests/test_heaps.py` to assert the literal array after `heapify([3, 1, 4, 2])`, which is `[4, 2, 3, 1]`.
3. Rewrite the `len` and `>= 1` checks in `tests/test_curriculum_completion.py` to literal lists, a literal cover, and the literal Huffman code lengths.
4. In `tests/test_binary_search_trace_fixtures.py`, assert the literal frame list for the `present` scenario.
5. Add one test per untested function with a small input and a literal output. For `locality_scan_benchmark` and anything that measures time, assert the shape of the result, not the timing.

Acceptance.
- [ ] `rg -n "__doc__" tests` returns nothing.
- [ ] For every function in the F-L-4 list, `rg -n "<name>\(" tests` returns an `assert ... ==` line.
- [ ] `pytest -q` passes and the collected count rises above 238.

Guardrails. Do not change library code to make a test pass unless the test found a defect. If it did, fix the defect in its own commit first.

#### WP-L-06. Add trace hooks to the lesson algorithms

Goal. Each function whose lesson shows states the public API does not return can emit those states through an optional `trace_sink`, the way `binary_search` does.

Why. F-C-3 and F-L-7. WP-C-03 consumes these hooks. Stack, queue, insertion sort, and Fibonacci frames are not in scope. Their frames follow from public calls, so WP-C-03 computes them by calling `push`, `pop`, `enqueue`, `dequeue`, and `fibonacci_modulo` directly.

Files. `sorting/merge_sort.py`, `sorting/quick_sort.py`, `heaps/heapsort.py`, `graphs/adjacency_list.py` (`breadth_first_order`), `trees/bst.py` (`insert`), `hash_tables/chaining.py` (`__setitem__`), `union_find/disjoint_set.py`, `linear/dynamic_array.py`, a new `bitsandbytes/tracing.py`.

Steps.
1. In `tracing.py`, define a frozen dataclass `TraceEvent(kind: str, values: dict[str, object])` and the alias `TraceSink = Callable[[TraceEvent], None]`.
2. Add `trace_sink: TraceSink | None = None` as a keyword-only parameter to each function. When it is `None`, the function must not build any event. Emit one event per step a learner would write down. The kinds are a split, a merge take, a partition swap, a sift, an enqueue, a dequeue, a bucket write, a parent link, and a resize copy.
3. For methods on containers, accept the sink on the constructor as `trace_sink` and store it.
4. Write `tests/test_trace_events.py`. For each hooked function, assert the literal event list for one small input.
5. Update the Cost blocks to state that the sink adds one call per emitted event.

Acceptance.
- [ ] `pytest tests/test_trace_events.py -q` passes with one test per hooked function, eight in total.
- [ ] `pytest -q` passes with the existing tests unchanged.
- [ ] `python3 -m timeit -s "import random; from bitsandbytes.sorting.merge_sort import merge_sort; data = random.Random(0).sample(range(100000), 10000)" "merge_sort(data)"` run three times before and three times after the change has a median within 10 percent. Paste the six lines.

Guardrails. Keyword-only parameters. No positional change. No new dependency.

#### WP-L-07. Bound the comparisons in the types

Goal. `mypy --strict` accepts the ordered containers and sorts, and a caller gets a type error for an unorderable key.

Why. F-L-6.

Files. A new `bitsandbytes/typing.py`, `trees/bst.py`, `trees/llrb.py`, `sorting/*.py`, `heaps/*.py`, `search/binary_search.py`.

Steps.
1. Define `class SupportsLessThan(Protocol)` with `def __lt__(self, other: Any, /) -> bool: ...` in `typing.py`, and `K = TypeVar("K", bound=SupportsLessThan)`.
2. Bind the type variables in the ordered modules to `SupportsLessThan`.
3. Remove those modules from the mypy override list from WP-L-01.

Acceptance.
- [ ] `mypy` exits 0 with the override list shorter than before. Paste the count before and after.
- [ ] A scratch file that inserts `object()` into a `BinarySearchTree` fails `mypy` with an error that names `SupportsLessThan`. Paste the error. Runtime behavior is unchanged.

Guardrails. No runtime behavior change.

#### WP-L-08. Remove the duplicates and loose ends

Goal. One stack type, both Dijkstras exported under names that say what they are, and no impossible assert.

Why. F-L-7.

Files. `stacks/stack.py`, `stacks/algorithm_stack.py`, `stacks/min_stack.py`, `stacks/next_greater.py`, `stacks/__init__.py`, `graphs/__init__.py`, `graphs/adjacency_list.py`, `graphs/algorithms.py`, `approximate/structures.py`, `heaps/priority_queue.py`, the guide files whose front matter names `algorithm_stack`.

Steps.
1. Let `Stack(limit=None)` mean unbounded. Migrate `MinStack` and `next_greater` to `Stack(limit=None)` and delete `algorithm_stack.py`. Update `stacks/__init__.py`, the guide front matter, and `scripts/build_guide_lessons.py` if it imports it.
2. Export `dijkstra_distances` and `dijkstra_distances_heap` from `graphs/__init__.py`. Make both summaries state the same bound as their Cost blocks.
3. Replace `assert self.previous is not None or True` with the condition the frame needs, or delete the assert.
4. Make `decrease_key` raise on an equal priority or change the message to `must not be larger`. Pick one and add a test.
5. Add one module docstring sentence to `linked_lists/reviewers.py` that says `ReviewersList` is a circular list with its own node type and names the lesson that uses it. If no lesson names it, delete the module and its test.

Acceptance.
- [ ] `rg -n "AlgorithmStack|algorithm_stack" bitsandbytes guide scripts tests` returns nothing.
- [ ] `rg -n "ReviewersList" guide bitsandbytes` returns either a lesson that names it or nothing at all.
- [ ] `python3 guide/check_lessons.py` prints `check_lessons: ok`.
- [ ] `pytest -q` passes and includes a test for the `decrease_key` behavior you chose.

Guardrails. Keep `Stack`'s default limit of 10 so existing lessons about bounded stacks stay true.

#### WP-L-09. Generate the cost reference from the library

Goal. The reference page lists every public function with its stated time cost and the lesson that teaches it, generated from the docstrings.

Why. F-UI-6 and F-L-3. Depends on WP-L-02.

Files. A new `scripts/build_cost_reference.py`, a new `site/src/data/cost-reference.json`, `site/src/app/reference/page.tsx`, `site/src/components/reference-search.tsx`, `site/package.json`.

Steps.
1. Write the script. For each public function and method with a `Cost` block, emit the module, the name, the first time bound in the block, the memory line, and the lesson slug whose front matter names the module. Fail if a module has no lesson.
2. Add `--check` and put it in the `build` chain.
3. Render the table on `/reference` under the glossary with the same search box filtering it.

Acceptance.
- [ ] `python3 scripts/build_cost_reference.py --check` exits 0.
- [ ] `/reference` shows a row count equal to the number of `Cost` blocks the script found. Paste both numbers.
- [ ] Typing `merge_sort` in the reference search shows the row and its lesson link.
- [ ] HTML gzip for `/reference` stays under 40960.

Guardrails. Reference mode only. No instruction or opinion in the generated rows.

## Suggested order

1. WP-UI-01, WP-UI-08, WP-UI-05, WP-C-01. Each is small and corrects something a learner sees today.
2. WP-L-01 and WP-UI-11. The gates protect every later change.
3. WP-UI-02, WP-UI-03, WP-UI-04. The lesson page, the menu, and the colors are what a learner touches most.
4. WP-L-02, WP-L-03, WP-L-05. The library becomes honest and importable before lessons lean on it.
5. WP-L-06, then WP-C-03, WP-C-02, WP-C-04, WP-C-06, WP-C-10. The generated lessons become computed, transferable, runnable, defined in order, and readable.
6. WP-C-05 in six batches. Each batch fills the learner's path from the front.
7. WP-UI-06, WP-UI-07, WP-UI-09, WP-UI-10, WP-C-09. Progress, search, and practice kinds depend on the content being there.
8. WP-L-04, WP-L-07, WP-L-08, WP-L-09, WP-C-07, WP-C-08. Consistency and the generated references close the review.

## Operator-only items

- Recruit three to five learners and run `docs/formative-learner-review-protocol.md`. No package in this guide replaces that evidence.
- Decide whether the 18 reference pages stay after WP-C-07 moves their unique facts into the sequence.
- Decide whether `partial` lessons should read `Full lesson`, or whether a third label is needed between `Overview` and the pilot's bar.
- Decide whether `push` should return the item, `None`, or a token across the library. WP-L-04 records the current mix.
- Decide whether to publish the library to PyPI after WP-L-01 adds a build backend.

## Appendix. Commands

Build and validate the site:

```bash
cd site && npm install --no-audit --no-fund && npm run build
```

Serve the production build for browser checks:

```bash
cd site && npx next start -p 3000
```

Run the Python tests:

```bash
python3 -m pip install --user pytest && python3 -m pytest -q
```

Check the lesson files and the generator:

```bash
python3 guide/check_lessons.py && python3 scripts/build_guide_lessons.py --check
```

Regenerate the readiness audit:

```bash
cd site && npm run report:readiness
```

Count lesson words after the front matter:

```bash
for f in guide/*.md; do
	w=$(awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$f" | wc -w)
	echo "$w $f"
done | sort -n
```

Count definitions and `Cost` mentions in the library:

```bash
rg -c '^\s*def [a-z_]+\(' bitsandbytes --glob '!__init__.py' | awk -F: '{s+=$2} END {print s}'
rg -c 'Cost' bitsandbytes --glob '!__init__.py' | awk -F: '{s+=$2} END {print s}'
```

Rendered contrast and tap-target audit. The review ran a `puppeteer-core` script against these routes at 1440 by 900 and 390 by 844. For each visible text node it resolved the nearest opaque background, computed the WCAG ratio, and reported nodes under 4.5:1 (3:1 for large text). It also listed controls under 44 px, heading order, landmarks, form labels, the first eight tab stops, and the home search results for six terms. WP-UI-02 adds that script to `site/scripts/` so the numbers in this guide can be rerun.

```text
/
/lessons/input-size-and-operation-counts
/lessons/cost-models
/lessons/binary-search
/lessons/merge-sort
/reference
/readiness
/python-foundations
/lessons/does-not-exist
/lessons/stacks
```
