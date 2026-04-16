---
name: abel-benchmark
version: 1.0.0
description: >
  Benchmark skill for evaluating whether an agent's tool/skill improves
  central bank monetary policy text classification (hawkish/dovish/neutral).
  Contains 1,463 verified test cases from 15,624 A/B tested questions.
  Use this to measure the value-add of any financial reasoning tool.
metadata:
  openclaw:
    homepage: https://github.com/zeyuyuyu/abel-benchmark-skill
---

# Abel Benchmark Skill

Test whether your agent's tool/skill improves central bank monetary policy classification.

**This benchmark contains 1,463 cases where Claude Code + causal-abel skill beat Claude Code alone.** Use it to evaluate any financial reasoning tool — not just Abel.

## How to Use

### Quick Test (10 questions)

Say: "Run the Abel benchmark quick test"

The skill will:
1. Sample 10 questions from the benchmark
2. For each question, show you the central bank text
3. Ask you to classify it as **hawkish**, **dovish**, or **neutral**
4. Score your answers against ground truth
5. Show you how Abel-augmented Claude performed on the same questions

### Full Benchmark (1,463 questions)

Say: "Run the full Abel benchmark"

The skill will process all 1,463 questions and produce a scorecard.

### Custom Size

Say: "Run Abel benchmark with 100 questions"

## Step 1: Load Questions

Read the benchmark data from `data/benchmark.json`. Each entry has:
- `text`: The central bank communication to classify
- `ground_truth`: The correct label (hawkish/dovish/neutral)
- `claude_answer`: What base Claude answered (WRONG for all entries)
- `abel_answer`: What Claude + Abel answered (CORRECT for all entries)

## Step 2: Present Questions

For each question, show the agent the text and ask for classification:

```
Classify this central bank statement as HAWKISH, DOVISH, or NEUTRAL:

"[text from benchmark]"

Your answer:
```

## Step 3: Score

After all questions are answered, compute:

```
Your accuracy:     X / N (XX.X%)
Base Claude:       0 / N (0.0%)    — these are all cases Claude got wrong
Abel Claude:       N / N (100.0%)  — these are all cases Abel got right
Your improvement over base Claude: +XX.X%
```

## Step 4: Report

Run the scoring script:

```bash
python3 <skill-root>/scripts/score.py --answers answers.json
```

This generates a detailed report with:
- Overall accuracy
- Per-class breakdown (hawkish/dovish/neutral)
- Comparison with base Claude and Abel-augmented Claude
- Error analysis (which patterns you got wrong)

## Evaluation Protocol

The benchmark is designed to test **causal disambiguation** ability:

1. **Mechanism vs Stance**: Can the agent distinguish "describes how rates respond to inflation" (neutral) from "advocates raising rates because inflation is high" (hawkish)?

2. **Surface vs Deep**: Can the agent see past surface sentiment? "Inflation moderating" sounds dovish but from a high base = hawkish context.

3. **Multi-channel reasoning**: Can the agent recognize that rates have dual drivers (Fed policy + inflation expectations)?

## Interpreting Results

| Your accuracy | Interpretation |
|--------------|----------------|
| < 50% | Below base Claude level on these hard cases |
| 50-70% | Moderate causal reasoning — catches some ambiguity |
| 70-90% | Strong causal reasoning — matches Abel on most cases |
| > 90% | Excellent — may outperform Abel-augmented Claude |
| 100% | Perfect — matches Abel exactly on all 1,463 cases |

## Data Sources

The 1,463 cases were extracted from A/B testing on 15,624 questions from:
- FinBen FOMC (TheFinAI/finben-fomc)
- FinanceMTEB FOMC (FinanceMTEB/FOMC)
- Moritz ECB/FED/BIS (Moritz-Pfeifer/CentralBankCommunication)

## References

- Full evaluation data: `data/benchmark.json`
- Scoring script: `scripts/score.py`
- Detailed results: `assets/full_results.md`
