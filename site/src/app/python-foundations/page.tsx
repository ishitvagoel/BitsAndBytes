import Link from "next/link";

export const metadata = {
  title: "Python foundations for the guide | Bits and Bytes",
  description: "An optional refresher on lists, indexes, loops and functions used in the algorithms guide.",
};

export default function PythonFoundationsPage() {
  return (
    <main id="main-content" className="support-page python-bridge" tabIndex={-1}>
      <Link className="back-link" href="/readiness">← Python readiness check</Link>
      <p className="eyebrow">OPTIONAL FOUNDATION · ABOUT 10 MINUTES</p>
      <h1>Python basics used in this guide</h1>
      <p className="support-lede">You do not need to know data structures or algorithms first. This short bridge covers the Python reading skills the lessons use, with one small example for each.</p>

      <article className="bridge-content">
        <section>
          <h2>Names hold values</h2>
          <p>An assignment gives a name a value. Later lines can read that value or assign a new one.</p>
          <pre><code>{"count = 2\ncount = count + 1\n# count is now 3"}</code></pre>
          <p>Read the second line as: take the current value of <code>count</code>, add one, and store the result back under that name.</p>
        </section>

        <section>
          <h2>Lists keep ordered items</h2>
          <p>Python lists are ordered. Indexing starts at zero, so the first item is at index 0 and the second is at index 1.</p>
          <pre><code>{"values = [4, 7, 9]\nfirst = values[0]   # 4\nsecond = values[1]  # 7\nsize = len(values)  # 3"}</code></pre>
          <p>An index is a position; a value is what is stored at that position. Those are different things.</p>
        </section>

        <section>
          <h2>Loops repeat work</h2>
          <p>A <code>for</code> loop visits each item in an iterable. The indented lines belong to the loop and run once per item.</p>
          <pre><code>{"total = 0\nfor value in values:\n    total = total + value\n# total is 20"}</code></pre>
          <p>When estimating work, first count how many times the loop body runs. Nested loops may repeat the body more times.</p>
        </section>

        <section>
          <h2>Functions take inputs and return results</h2>
          <p>A function groups steps behind a name. Parameters receive inputs; <code>return</code> sends a result back to the caller.</p>
          <pre><code>{"def contains_two(values):\n    for value in values:\n        if value == 2:\n            return True\n    return False\n\nanswer = contains_two([1, 2, 3])  # True"}</code></pre>
          <p>This function may inspect one item or every item. Later lessons explain how to describe that work with a cost model.</p>
        </section>

        <section>
          <h2>Read a trace one line at a time</h2>
          <p>For each line, track the names and values that matter. On a loop, record the current item. On a condition, follow the branch whose expression is true. Stop when the function returns or the loop has no more items.</p>
          <p>Try the readiness check again if you want feedback, or continue directly to the pilot. The bridge is a reference, not a prerequisite gate.</p>
        </section>
      </article>

      <div className="bridge-actions">
        <Link className="button button-primary" href="/lessons/binary-search">Start the learning pilot <span aria-hidden="true">→</span></Link>
        <Link href="/">Browse every lesson</Link>
      </div>
    </main>
  );
}
