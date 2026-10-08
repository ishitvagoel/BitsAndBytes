import { ReferenceSearch, type GlossaryTerm, type ReferenceRow } from "@/components/reference-search";

const comparisons: ReferenceRow[] = [
  {
    name: "bisect_left",
    purpose: "Find the first valid insertion point in an already sorted sequence.",
    behavior: "Binary search takes O(log n) time; values equal to the target stay to the right of the returned position.",
    sourceLabel: "Python bisect documentation",
    sourceUrl: "https://docs.python.org/3/library/bisect.html",
    lessonSlug: "binary-search",
    lessonTitle: "Binary search",
  },
  {
    name: "insort_left",
    purpose: "Insert a value into a sorted Python list while keeping it sorted.",
    behavior: "The position search is O(log n), but list insertion can move later values, so the complete operation is O(n).",
    sourceLabel: "Python bisect documentation",
    sourceUrl: "https://docs.python.org/3/library/bisect.html",
    lessonSlug: "binary-search",
    lessonTitle: "Binary search",
  },
  {
    name: "collections.deque",
    purpose: "Add or remove items at both ends, such as a FIFO queue or a sliding window.",
    behavior: "Endpoint appends and pops are approximately O(1); a deque is not designed for fast access to arbitrary middle positions.",
    sourceLabel: "Python collections documentation",
    sourceUrl: "https://docs.python.org/3/library/collections.html#collections.deque",
    lessonSlug: "queues-and-deque",
    lessonTitle: "Queues and deques",
  },
  {
    name: "heapq",
    purpose: "Repeatedly retrieve the smallest pending value from a priority queue.",
    behavior: "The list keeps a min-heap ordering; the smallest value is at index 0, while the remaining values are not fully sorted.",
    sourceLabel: "Python heapq documentation",
    sourceUrl: "https://docs.python.org/3/library/heapq.html",
    lessonSlug: "heaps",
    lessonTitle: "Heaps",
  },
  {
    name: "functools.lru_cache",
    purpose: "Reuse results from repeated calls to a function with the same arguments.",
    behavior: "Stores recent function results up to a configurable limit; arguments must be hashable.",
    sourceLabel: "Python functools documentation",
    sourceUrl: "https://docs.python.org/3/library/functools.html#functools.lru_cache",
    lessonSlug: "dynamic-programming",
    lessonTitle: "Dynamic programming",
  },
];

const terms: GlossaryTerm[] = [
  { term: "Algorithm invariant", definition: "A statement that remains true before and after each step; it helps show why an algorithm is correct.", lessonSlug: "binary-search", lessonTitle: "Binary search" },
  { term: "Lower bound", definition: "The first position whose value is not less than a target; the target may be absent.", lessonSlug: "binary-search", lessonTitle: "Binary search" },
  { term: "Upper bound", definition: "The first position whose value is greater than a target; subtracting the lower bound gives the duplicate count.", lessonSlug: "binary-search", lessonTitle: "Binary search" },
  { term: "Stable sort", definition: "A sort that preserves the original relative order of items with equal keys.", lessonSlug: "sorting", lessonTitle: "Sorting" },
  { term: "Hash collision", definition: "Two distinct keys map to the same hash-table location and need an additional resolution step.", lessonSlug: "hash-table", lessonTitle: "Hash tables" },
  { term: "Heap invariant", definition: "Each parent has priority over its children; this exposes the next minimum or maximum without fully sorting all values.", lessonSlug: "heaps", lessonTitle: "Heaps" },
  { term: "Path compression", definition: "A disjoint-set optimization that makes nodes point closer to their representative during a find operation.", lessonSlug: "union-find", lessonTitle: "Union-find" },
  { term: "Topological order", definition: "An ordering of a directed acyclic graph in which every edge points from an earlier item to a later item.", lessonSlug: "graphs", lessonTitle: "Graphs" },
  { term: "Dynamic programming", definition: "A way to solve problems by storing results for overlapping subproblems instead of recomputing them.", lessonSlug: "dynamic-programming", lessonTitle: "Dynamic programming" },
  { term: "Greedy choice", definition: "A locally preferred step; a correctness argument must show why choosing it still permits a globally optimal result.", lessonSlug: "greedy-algorithms", lessonTitle: "Greedy algorithms" },
  { term: "Backtracking", definition: "Explore a choice, continue while it can lead to a solution, and undo it when that path cannot succeed.", lessonSlug: "backtracking-and-array-patterns", lessonTitle: "Backtracking and array patterns" },
  { term: "Prefix sum", definition: "A running total that can turn a range-sum query into a subtraction of two prefix values.", lessonSlug: "backtracking-and-array-patterns", lessonTitle: "Backtracking and array patterns" },
  { term: "False positive", definition: "An approximate structure reports that an item may be present even though it is absent; a false negative may be ruled out by its guarantee.", lessonSlug: "range-queries-and-approximate-structures", lessonTitle: "Range queries and approximate structures" },
];

export default function ReferencePage() {
  return (
    <main id="main-content" className="reference-page" tabIndex={-1}>
      <p className="eyebrow">ALGORITHM AND PYTHON REFERENCE</p>
      <h1>Glossary and library choices</h1>
      <p className="reference-intro">Search short definitions and compare Python tools with the algorithm idea they support. These reference lookups do not change course progress.</p>
      <ReferenceSearch comparisons={comparisons} terms={terms} />
    </main>
  );
}
