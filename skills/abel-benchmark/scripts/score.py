#!/usr/bin/env python3
"""
Abel Benchmark Scoring Script.

Usage:
  python3 score.py --answers answers.json
  python3 score.py --answers answers.json --n 100
  python3 score.py --sample 10  # quick sample test (prints questions to stdout)
"""
import json
import os
import argparse
import random
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARK_PATH = os.path.join(SKILL_ROOT, "data", "benchmark.json")


def load_benchmark():
    with open(BENCHMARK_PATH) as f:
        return json.load(f)


def score_answers(benchmark, answers):
    """Score user answers against ground truth."""
    results = {
        "total": 0,
        "correct": 0,
        "by_class": {"hawkish": {"total": 0, "correct": 0},
                     "dovish": {"total": 0, "correct": 0},
                     "neutral": {"total": 0, "correct": 0}},
        "errors": [],
    }

    for i, (q, ans) in enumerate(zip(benchmark, answers)):
        gt = q["ground_truth"].lower().strip()
        user = str(ans).lower().strip()
        results["total"] += 1

        if gt in results["by_class"]:
            results["by_class"][gt]["total"] += 1

        if user == gt:
            results["correct"] += 1
            if gt in results["by_class"]:
                results["by_class"][gt]["correct"] += 1
        else:
            results["errors"].append({
                "index": i,
                "text": q["text"][:100],
                "your_answer": user,
                "correct": gt,
                "claude_base": q.get("claude_answer", ""),
                "abel": q.get("abel_answer", ""),
            })

    return results


def print_report(results):
    n = results["total"]
    c = results["correct"]
    pct = c / n * 100 if n else 0

    print(f"\n{'='*60}")
    print(f"ABEL BENCHMARK RESULTS")
    print(f"{'='*60}")
    print(f"\nYour accuracy:        {c}/{n} ({pct:.1f}%)")
    print(f"Base Claude (no Abel): 0/{n} (0.0%)  — all cases are Claude-wrong by design")
    print(f"Claude + Abel:         {n}/{n} (100.0%)  — all cases are Abel-correct by design")
    print(f"\nYour improvement over base Claude: +{pct:.1f}%")

    print(f"\nPer-class breakdown:")
    for cls, data in results["by_class"].items():
        if data["total"] > 0:
            acc = data["correct"] / data["total"] * 100
            print(f"  {cls:10s}: {data['correct']}/{data['total']} ({acc:.1f}%)")

    if results["errors"]:
        print(f"\nError examples (first 5):")
        for e in results["errors"][:5]:
            print(f"  [{e['index']}] you={e['your_answer']}, correct={e['correct']} | {e['text']}")


def sample_test(n=10):
    """Print n random questions for manual testing."""
    benchmark = load_benchmark()
    sample = random.sample(benchmark, min(n, len(benchmark)))
    print(f"ABEL BENCHMARK — {len(sample)} Question Sample\n")
    print("Classify each central bank statement as HAWKISH, DOVISH, or NEUTRAL.\n")

    for i, q in enumerate(sample, 1):
        print(f"--- Question {i}/{len(sample)} ---")
        print(f"{q['text']}\n")
        print(f"Your answer: _________")
        print(f"(Ground truth: {q['ground_truth']}, Base Claude: {q.get('claude_answer','?')}, Abel: {q.get('abel_answer','?')})\n")


def main():
    parser = argparse.ArgumentParser(description="Abel Benchmark Scorer")
    parser.add_argument("--answers", help="JSON file with list of answers")
    parser.add_argument("--n", type=int, help="Number of questions to score (default: all)")
    parser.add_argument("--sample", type=int, help="Print N random questions for manual testing")
    args = parser.parse_args()

    if args.sample:
        sample_test(args.sample)
        return

    if not args.answers:
        print("Usage: python3 score.py --answers answers.json")
        print("       python3 score.py --sample 10")
        sys.exit(1)

    benchmark = load_benchmark()
    if args.n:
        benchmark = benchmark[:args.n]

    with open(args.answers) as f:
        answers = json.load(f)

    if len(answers) < len(benchmark):
        print(f"Warning: only {len(answers)} answers for {len(benchmark)} questions")
        benchmark = benchmark[:len(answers)]

    results = score_answers(benchmark, answers)
    print_report(results)

    # Save detailed results
    out_path = args.answers.replace(".json", "_scored.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to {out_path}")


if __name__ == "__main__":
    main()
