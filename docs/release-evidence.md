# Redesign implementation release evidence

Recorded 6 October 2026 for branch `codex/bitsandbytes-learning-redesign`. This records implementation evidence and remaining release gates; it does not authorize or perform a deployment.

## Verified in this workspace

- `python guide/check_lessons.py` passes for all 70 guide pages.
- `python scripts/build_lesson_crosswalk.py` generates 146 module mappings across the 70 lesson slugs.
- `python scripts/build_binary_search_traces.py` regenerates the pilot source excerpt and trace fixtures.
- Site curriculum validation passes: 70 lessons, unique lesson/objective IDs, valid prerequisite graph, slug coverage, source/test mappings, and five trace scenarios. Markdown validation resolves 91 local links.
- `npm run lint`, `npx tsc --noEmit`, `npm run build`, and `npm run test:progress` pass. The production build generates 77 static pages, including all 70 lesson routes. The rendered-link check validates 10,670 internal links/fragments across 76 generated HTML pages, and the critical learning-journey assertion checks the actual pilot next-lesson sequence.
- A read-only production-preview HTTP smoke test returned HTTP 200 and a titled page with main content for all 74 learner-facing routes: home, readiness, Python foundations, reference and 70 lesson URLs.
- `npm run build` includes a performance budget check for the optimized binary-search route. The latest measurement is 28,624 gzip bytes HTML, 185,592 gzip bytes JavaScript, 7,030 gzip bytes CSS, and 221,246 gzip bytes combined; configured local budgets pass. This is an optimized-build asset estimate, not a comparison with the old production site; the older baseline report needs a same-conditions comparison before P5-11 can close.
- `PYTHONPATH=../review-deps python -m pytest -q` passes all 236 tests. `python guide/check_lessons.py` passes all 70 lesson files, and `git diff --check` passes.
- Progress tests now cover per-objective rechecks, retained historical attempts, fresh due-review responses, strict imports and stale-write fallback. Full browser quota, cross-tab and export/import round-trip checks remain open.
- This implementation pass expanded `guide/42-binary-search-on-answer.md` into a worked Partially taught lesson with two exercises. Most of the 70 lesson routes remain below the full readiness rubric; route count and source mappings do not mean those lessons are complete.
- `npm run report:readiness` generates [`lesson-readiness-audit.md`](./lesson-readiness-audit.md) with one row per route: 66 Summary, 2 Partially taught, 1 Ready and 1 Reference. The generated rubric actions are a triage queue, not a substitute for lesson-by-lesson editorial review.

## Remaining release gates

- The first GitHub PR preview failed after Next.js had built: Vercel packaged its `.next` output before the repository's post-build static-artifact scripts tried to open `site/.next/server/app/index.html`. The follow-up keeps curriculum and Markdown validation in the build on Vercel, skips only those local-output-specific post-build checks there, and retains them in full for local production builds. The Vercel check must pass again after this fix.

- The production preview server starts on loopback and the HTTP route smoke test passes, but the cloud browser blocks navigation to both `127.0.0.1` and `localhost` with `ERR_BLOCKED_BY_CLIENT`. The local agent-browser Chrome installation previously failed certificate validation. No tunnel or deployment was created.
- Responsive widths, browser zoom, keyboard/focus behavior, touch targets, overflow and home → lesson → revisit → home still need a real browser pass.
- Progress persistence, version recheck and export/import need a real-browser round-trip.
- Formative learning review needs 3–5 actual learners, pre/post transfer prompts, delayed recall and response-driven revisions. No participant contact or recruitment was performed.
- The performance baseline is static production-build asset weight. Live Vercel timing and Core Web Vitals (TTFB, LCP, CLS and INP) remain unmeasured.
- New focused topic pages remain honestly labelled Summary; they need full worked traces, feedback-bearing practice and learner evidence before being promoted to course-ready. The binary-search-on-answer follow-on is labelled Partially taught and also needs learner evidence.

## Release scope

Accounts, cross-device synchronization, AI tutoring, arbitrary Python execution, leaderboards and a full LMS remain deferred. Browser visual/interaction checks, formative learner review and matched production performance comparison are TODO. This implementation has not been deployed or published.
