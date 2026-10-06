# Browser acceptance run sheet

Use this against a reachable preview build before closing P2-21, P2-24, P2-25, P3-10 or P5-12. Record browser/version, operating system, viewport, zoom, result, and any issue. A production build and static route assertions do not replace these checks.

## Viewport and reading checks

Run at 320, 390, 768 and 1440 CSS-pixel viewport widths. At each width:

- [ ] Home, readiness, Python foundations, reference, and the binary-search lesson render without page-wide horizontal scrolling.
- [ ] Resize the viewport and zoom to 200%; repeat at 400% effective zoom where supported. Text reflows and controls remain reachable.
- [ ] Open the course navigation disclosure on mobile and collapse/expand the desktop course rail. Content remains readable and the current lesson is identifiable.
- [ ] Inspect long Python identifiers, code blocks, tables, glossary results and the trace. They wrap or scroll within their own container without obscuring neighboring content.
- [ ] Verify no sticky/fixed element covers headings, anchors, answer feedback, or focused controls.
- [ ] Check touch targets on a touch-capable device; every control is comfortably targetable and does not depend on hover.

## Keyboard and assistive checks

- [ ] Reload and press Tab. The skip link appears first, moves focus to main content, and focus indicators remain visible.
- [ ] Complete home → readiness (skip or finish) → binary-search lesson → trace controls → practice answers → next lesson → home using only the keyboard.
- [ ] Operate all native disclosures and selectors with keyboard input; focus order follows reading order and never becomes trapped.
- [ ] Confirm headings are hierarchical, buttons/links have understandable names, status/feedback is announced, and correctness is not conveyed by color alone.
- [ ] Enable reduced motion and confirm no required information or interaction depends on animation.

## URL, progress and import/export checks

- [ ] Open every legacy URL and every generated canonical lesson URL; each loads the intended page, with no loops or dead ends.
- [ ] Save a non-default lesson section, navigate away, return and refresh. Resume points to the saved lesson and section.
- [ ] Submit wrong and correct practice answers. Attempts, due-review state, and recheck state remain distinct after navigation and refresh.
- [ ] Change a lesson content version in a test fixture. Old attempts remain, and the updated objective asks for a recheck.
- [ ] Export progress, clear site storage, import the export, and compare resume, attempt, trace and exercise-answer state. Reject malformed, unsupported and wrong-shape files without corrupting current state.
- [ ] Reset local progress and verify the UI explains that data is device-local and has been cleared.

## Evidence record

| Browser / device | Width and zoom | Checks passed | Issues and reproduction | Follow-up |
|---|---|---|---|---|
| Pending reachable preview | — | — | — | Do not mark acceptance items complete before recording an actual run. |
