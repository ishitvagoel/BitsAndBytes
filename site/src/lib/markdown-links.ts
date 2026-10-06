/** Resolve the filename-style links used by the repository's guide Markdown. */
export function resolveLessonMarkdownHref(href: string, lessonSlugs: ReadonlySet<string>): string | null {
  const match = /^([^?#]+\.md)([?#].*)?$/i.exec(href);
  if (!match) return null;

  const basename = match[1].split(/[\\/]/).at(-1) ?? "";
  const filenameSlug = basename.replace(/\.md$/i, "");
  const candidates = [filenameSlug, filenameSlug.replace(/^\d+-/, "")];
  const slug = candidates.find((candidate) => lessonSlugs.has(candidate));
  return slug ? `/lessons/${slug}${match[2] ?? ""}` : null;
}
