import Link from "next/link";

export default function NotFound() {
  return (
    <main id="main-content" className="not-found-page">
      <p className="eyebrow">PAGE NOT FOUND</p>
      <h1>This lesson link has moved or no longer exists.</h1>
      <p>Use the course guide to find the topic you were looking for.</p>
      <Link className="button button-primary" href="/">Open the course guide</Link>
    </main>
  );
}
