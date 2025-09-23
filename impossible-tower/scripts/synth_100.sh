#!/usr/bin/env bash
set -euo pipefail

MODE="local"
OUTPUT_DIR="data/synth_50"

for arg in "$@"; do
  case "$arg" in
    --ci)
      MODE="ci"
      OUTPUT_DIR="/tmp/itower_ci"
      ;;
    --local)
      MODE="local"
      OUTPUT_DIR="data/synth_50"
      ;;
  esac
done

mkdir -p "$OUTPUT_DIR"

python -m data_gen.make_dataset \
  --out "$OUTPUT_DIR" \
  --n-scenes 50 \
  --pos-frac 0.5 \
  --views 4 \
  --seed 42

echo "Synthetic dataset generated at $OUTPUT_DIR (mode=$MODE)"
