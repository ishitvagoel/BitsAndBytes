export type LessonSection = { id: string; title: string; level: 2 | 3 };

export function headingId(title: string): string {
  return title
    .toLocaleLowerCase("en")
    .replace(/[`*_~]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export function getSections(markdown: string): LessonSection[] {
  const sections: LessonSection[] = [];
  let inFence = false;
  const seen = new Map<string, number>();
  for (const line of markdown.split("\n")) {
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;
    const match = /^(#{2,3})\s+(.+?)\s*#*\s*$/.exec(line);
    if (!match) continue;
    const title = match[2].replace(/`([^`]+)`/g, "$1").replace(/[*_~]/g, "").trim();
    const baseId = headingId(title);
    const count = seen.get(baseId) ?? 0;
    seen.set(baseId, count + 1);
    sections.push({ id: count === 0 ? baseId : `${baseId}-${count + 1}`, title, level: match[1].length as 2 | 3 });
  }
  return sections;
}
