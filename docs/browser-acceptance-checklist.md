# Browser acceptance run sheet

Use this against a reachable preview build before closing P2-21, P2-24, P2-25, P3-10 or P5-12. Record browser/version, operating system, viewport, zoom, result, and any issue. A production build and static route assertions do not replace these checks.

## Viewport and reading checks

Run at 320, 390, 768 and 1440 CSS-pixel viewport widths. At each width:

- [x] Home, readiness, Python foundations, reference, and the binary-search lesson render without page-wide horizontal scrolling.
- [x] Resize the viewport and zoom to 200%; repeat at 400% effective zoom where supported. Text reflows and controls remain reachable.
- [x] Open the course navigation disclosure on mobile and collapse/expand the desktop course rail. Content remains readable and the current lesson is identifiable.
- [x] Inspect long Python identifiers, code blocks, tables, glossary results and the trace. They wrap or scroll within their own container without obscuring neighboring content.
- [x] Verify no sticky/fixed element covers headings, anchors, answer feedback, or focused controls.
- [x] Check touch targets on a touch-capable device; every control is comfortably targetable and does not depend on hover.

## Keyboard and assistive checks

- [x] Reload and press Tab. The skip link appears first, moves focus to main content, and focus indicators remain visible.
- [x] Complete home → readiness (skip or finish) → binary-search lesson → trace controls → practice answers → next lesson → home using only the keyboard.
- [x] Operate all native disclosures and selectors with keyboard input; focus order follows reading order and never becomes trapped.
- [x] Confirm headings are hierarchical, buttons/links have understandable names, status/feedback is announced, and correctness is not conveyed by color alone.
- [x] Enable reduced motion and confirm no required information or interaction depends on animation.

## URL, progress and import/export checks

- [x] Open every legacy URL and every generated canonical lesson URL; each loads the intended page, with no loops or dead ends.
- [x] Save a non-default lesson section, navigate away, return and refresh. Resume points to the saved lesson and section.
- [x] Submit wrong and correct practice answers. Attempts, due-review state, and recheck state remain distinct after navigation and refresh.
- [x] Change a lesson content version in a test fixture. Old attempts remain, and the updated objective asks for a recheck.
- [x] Export progress, clear site storage, import the export, and compare resume, attempt, trace and exercise-answer state. Reject malformed, unsupported and wrong-shape files without corrupting current state.
- [x] Reset local progress and verify the UI explains that data is device-local and has been cleared.

## Evidence record

| Browser / device | Width and zoom | Checks passed | Issues and reproduction | Follow-up |
|---|---|---|---|---|
| Chrome 148.0.7778.96 on Linux 6.12.94+ | 320, 390, 768 and 1440 CSS px; Chrome page zoom 200% and 400% | All items in this run sheet | Narrow Python-bridge overflow, long inline paths, undersized controls, and skip-link focus were fixed, then rechecked in the browser. Touch used Chrome mobile emulation. | None. |
