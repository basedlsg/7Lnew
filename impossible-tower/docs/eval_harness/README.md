# Evaluation Harness

The evaluation harness aggregates metrics for Impossible Tower runs.

- `src/model/train_vertex/eval.py` implements the CLI.
- `scripts/run_eval.sh` orchestrates small vs. medium dataset runs.
- Nightly CI triggers the harness via the `nightly-evals` job when scheduled.

## Usage

```bash
bash scripts/run_eval.sh small
```

Results are written to `docs/eval_results/` with timestamped Markdown tables.

- Latest dataset: gs://impossible-tower-data/itower/v0.1/synth_500
- Daily autogen: gs://impossible-tower-data/itower/<YYYY-MM-DD>/synth_500
- Latest results: docs/eval_results/eval-20250919-121706.md
