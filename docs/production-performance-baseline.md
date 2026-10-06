# Binary-search production-build performance baseline

Measured 6 October 2026 from the optimized Next.js production build in this repository.

## Observed route weight

Command: `cd site && npm run build && npm run measure:performance`

| Route asset | Raw bytes | Gzip bytes | Budget (gzip) | Result |
|---|---:|---:|---:|---|
| `/lessons/binary-search` HTML | 215,211 | 28,624 | 40 KiB | Pass |
| Unique JavaScript referenced by the route | 604,812 | 185,592 | 200 KiB | Pass |
| Unique CSS referenced by the route | 30,313 | 7,030 | 10 KiB | Pass |
| Initial HTML + JavaScript + CSS estimate | 850,336 | 221,246 | 256 KiB | Pass |

The measurement script reads the static production HTML and its unique local JS/CSS assets, then applies gzip level 9. The totals are a reproducible transfer-size estimate; actual response compression, caching, fonts, image requests, and network conditions can change browser-observed bytes and timings.

## Budget rationale

Budgets are rounded above the observed baseline to leave room for ordinary content and framework variation while keeping the pilot route below 256 KiB for HTML plus first-load JS/CSS under gzip. Re-run the command after material page or dependency changes. Treat exceeding an individual budget as a review trigger; do not raise a budget without recording a new measured baseline and reason.

## Limits and remaining evidence

This is a production-build asset estimate, not an old-versus-redesigned comparison or live Vercel measurement. The previous local measurement on this branch was 218,667 gzip bytes; the current build is 2,579 bytes larger. Build revisions/dependencies and the browser-requested transfer set have not been held constant, so this delta is descriptive only. A one-byte HTML gzip variation occurred across repeated builds. It does not measure TTFB, LCP, CLS, INP, interaction responsiveness, or mobile-network behavior. The matched browser comparison, live Vercel timing and accessibility checks remain open until a reachable preview and comparable historical build are available.
