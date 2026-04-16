#!/usr/bin/env python3
"""
Run the Abel Benchmark programmatically.

Loads questions, lets a callable classifier answer them, scores results.
Designed for integration with agent frameworks.

Usage:
    from run_benchmark import run_benchmark

    def my_classifier(text: str) -> str:
        # Your agent/tool classifies the text
        return "hawkish"  # or "dovish" or "neutral"

    results = run_benchmark(my_classifier, n=100)
    print(f"Accuracy: {results['accuracy']:.1%}")
"""
import json
import os
import random
from typing import Callable, Optional

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARK_PATH = os.path.join(SKILL_ROOT, "data", "benchmark.json")


def load_benchmark(n: Optional[int] = None, shuffle: bool = False, seed: int = 42):
    """Load benchmark questions."""
    with open(BENCHMARK_PATH) as f:
        data = json.load(f)
    if shuffle:
        random.seed(seed)
        random.shuffle(data)
    if n:
        data = data[:n]
    return data


def run_benchmark(
    classifier: Callable[[str], str],
    n: Optional[int] = None,
    shuffle: bool = False,
    verbose: bool = True,
):
    """
    Run the benchmark with a custom classifier.

    Args:
        classifier: Function that takes text (str) and returns "hawkish", "dovish", or "neutral"
        n: Number of questions (None = all 1,463)
        shuffle: Randomize question order
        verbose: Print progress

    Returns:
        dict with accuracy, per_class, errors, comparison
    """
    questions = load_benchmark(n=n, shuffle=shuffle)
    total = len(questions)

    correct = 0
    by_class = {}
    errors = []

    for i, q in enumerate(questions):
        text = q["text"]
        gt = q["ground_truth"].lower().strip()
        answer = classifier(text).lower().strip()

        if gt not in by_class:
            by_class[gt] = {"total": 0, "correct": 0}
        by_class[gt]["total"] += 1

        if answer == gt:
            correct += 1
            by_class[gt]["correct"] += 1
        else:
            errors.append({
                "index": i, "text": text[:100],
                "answer": answer, "truth": gt,
            })

        if verbose and (i + 1) % 100 == 0:
            print(f"  [{i+1}/{total}] accuracy so far: {correct/(i+1)*100:.1f}%")

    accuracy = correct / total if total else 0

    results = {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "per_class": {
            cls: {
                "total": d["total"],
                "correct": d["correct"],
                "accuracy": d["correct"] / d["total"] if d["total"] else 0,
            }
            for cls, d in by_class.items()
        },
        "errors": errors[:20],
        "comparison": {
            "base_claude": 0.0,  # all cases are Claude-wrong by design
            "abel_claude": 1.0,  # all cases are Abel-correct by design
            "your_accuracy": accuracy,
            "vs_base": f"+{accuracy*100:.1f}%",
            "vs_abel": f"{(accuracy-1.0)*100:+.1f}%",
        },
    }

    if verbose:
        print(f"\n{'='*50}")
        print(f"Your accuracy: {correct}/{total} ({accuracy*100:.1f}%)")
        print(f"Base Claude:   0/{total} (0.0%)")
        print(f"Abel Claude:   {total}/{total} (100.0%)")
        for cls, d in results["per_class"].items():
            print(f"  {cls}: {d['correct']}/{d['total']} ({d['accuracy']*100:.1f}%)")

    return results


if __name__ == "__main__":
    # Demo: random classifier
    def random_classifier(text):
        return random.choice(["hawkish", "dovish", "neutral"])

    print("Running benchmark with random classifier (baseline)...")
    results = run_benchmark(random_classifier, n=100, shuffle=True)
    print(f"\nRandom baseline: {results['accuracy']*100:.1f}% (expected ~33%)")
