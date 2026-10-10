"use client";

import { useState } from "react";

export function ModuleList({ names }: { names: string[] }) {
  const [open, setOpen] = useState(false);
  if (names.length === 0) return null;
  const visible = names.length <= 4 || open ? names : names.slice(0, 4);
  return (
    <section className="module-list" aria-labelledby="module-list-title">
      <h2 id="module-list-title">Modules <span>{names.length}</span></h2>
      <ul>
        {visible.map((name) => <li key={name}><code>{name}</code></li>)}
      </ul>
      {names.length > 4 && (
        <button type="button" aria-expanded={open} onClick={() => setOpen((value) => !value)}>
          {open ? "Show fewer modules" : `Show all ${names.length} modules`}
        </button>
      )}
    </section>
  );
}
