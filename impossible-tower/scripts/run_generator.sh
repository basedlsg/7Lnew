#!/usr/bin/env bash
set -euo pipefail

DATE_PREFIX=$(date +%F)
OUTPUT="gs://${GCS_DATA_BUCKET:-impossible-tower-data}/itower/${DATE_PREFIX}/synth_${SCENE_COUNT:-500}"
SEED=${SEED_OVERRIDE:-$(date +%s)}

python -m data_gen.make_dataset \
  --out "$OUTPUT" \
  --n-scenes "${SCENE_COUNT:-500}" \
  --pos-frac 0.5 \
  --views 4 \
  --seed "$SEED"
