#!/usr/bin/env bash
set -euo pipefail

SPLIT="small"
if [ $# -ge 1 ]; then
  SPLIT="$1"
fi

case "$SPLIT" in
  small)
    DATASET_DIR="data/synth_50"
    ;;
  medium)
    DATASET_DIR="data/synth_200"
    ;;
  *)
    echo "Unknown split: $SPLIT" >&2
    exit 1
    ;;
esac

if [ ! -d "$DATASET_DIR" ]; then
  echo "Dataset $DATASET_DIR not found. Generate it with scripts/synth_100.sh" >&2
  exit 1
fi

python -m model.train_vertex.eval \
  --dataset-dir "$DATASET_DIR" \
  --output-dir "docs/eval_results"
