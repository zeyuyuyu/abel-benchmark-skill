# Abel Benchmark Skill

A Claude Code skill for testing whether an agent's tool/skill improves central bank monetary policy text classification.

Contains **1,463 verified test cases** from real A/B testing on 15,624 questions.

## Install

```bash
# Project-local
npx --yes skills add https://github.com/zeyuyuyu/abel-benchmark-skill/tree/main/skills --skill abel-benchmark -y

# Global
npx --yes skills add https://github.com/zeyuyuyu/abel-benchmark-skill/tree/main/skills --skill abel-benchmark -g -y
```

## Usage in Claude Code

```
> Run the Abel benchmark quick test
> Run the full Abel benchmark
> Run Abel benchmark with 100 questions
```

## Usage in Code

```python
from scripts.run_benchmark import run_benchmark

def my_classifier(text: str) -> str:
    # Your classification logic here
    return "hawkish"  # or "dovish" or "neutral"

results = run_benchmark(my_classifier, n=100)
print(f"Accuracy: {results['accuracy']:.1%}")
```

## What It Tests

Each question is a central bank statement that must be classified as **hawkish**, **dovish**, or **neutral**. These 1,463 cases are specifically the ones where:
- Claude Code alone gets it **wrong**
- Claude Code + Abel causal skill gets it **right**

They test **causal disambiguation** — can the agent distinguish mechanism descriptions from policy stances, and resolve multi-channel economic reasoning?

## Scoring

| Your accuracy | Interpretation |
|--------------|----------------|
| < 50% | Below base Claude level |
| 50-70% | Moderate causal reasoning |
| 70-90% | Strong — matches Abel on most cases |
| > 90% | Excellent — may surpass Abel |

## Source

Derived from [Abel Causal Advantage Benchmark](https://github.com/zeyuyuyu/abel-causal-advantage-benchmark). Data from FinBen FOMC, FinanceMTEB, Moritz ECB/FED/BIS.

## License

Apache 2.0
