# Evaluation Guide

## Metrics

| Metric | Description |
| ------ | ----------- |
| Accuracy@1 | Percentage of scenes where the model answers the binary question correctly |
| Program Pass Rate | Fraction of generated programs that satisfy the Z3 checker |
| Violation Rate | Average number of violated constraints per failed scene |
| Counterexample Rate | Percentage of failing scenes where a counterexample is provided |
| Cross-view Consistency | Probability that model answers are invariant to view permutations |

## Running the harness

Use the helper script to run the evaluation pipeline:

```bash
bash scripts/run_eval.sh small
```

This script invokes `python -m src.model.train_vertex.eval` with the appropriate dataset splits and collects metrics into `docs/eval_results/<timestamp>.md`.

## Interpreting results

- Aim for high Accuracy@1 and Program Pass Rate.
- Investigate scenes with high violation counts; inspect the emitted counterexamples.
- Review cross-view consistency to ensure the model is robust to camera orderings.

## Reporting

The evaluation script writes a Markdown table summarizing metrics and attaches run metadata (dataset version, model checkpoint, Vertex job IDs). Include the table when publishing releases or drafting research artifacts.


## Latest run

- Dataset: gs://impossible-tower-data/itower/v0.1/synth_500
- Results: docs/eval_results/eval-20250919-121706.md
