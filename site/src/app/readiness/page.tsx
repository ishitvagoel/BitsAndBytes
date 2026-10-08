import Link from "next/link";

import { ReadinessCheck } from "@/components/readiness-check";

export const metadata = {
  title: "Python readiness check | Bits and Bytes",
  description: "Check the small Python basics used in the Bits and Bytes algorithms guide.",
};

export default function ReadinessPage() {
  return (
    <main id="main-content" className="support-page" tabIndex={-1}>
      <Link className="back-link" href="/">← Course home</Link>
      <p className="eyebrow">OPTIONAL · ABOUT 3 MINUTES</p>
      <h1>Check the Python basics</h1>
      <p className="support-lede">The algorithms guide assumes you can read simple Python lists, loops and functions. This is a quick self-check so you can choose a comfortable starting point.</p>
      <ReadinessCheck />
    </main>
  );
}
