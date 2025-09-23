#!/usr/bin/env bash
set -euo pipefail

if [ -z "${GCP_PROJECT:-}" ] || [ -z "${BUCKET_NAME:-}" ]; then
  echo "GCP_PROJECT and BUCKET_NAME must be set" >&2
  exit 1
fi

gcloud config set project "$GCP_PROJECT"

cat <<MSG
Creating bucket gs://$BUCKET_NAME for Impossible Tower datasets.
MSG

gsutil mb -p "$GCP_PROJECT" -c STANDARD -l us-central1 "gs://$BUCKET_NAME" || echo "Bucket may already exist"

gsutil iam ch "serviceAccount:$SERVICE_ACCOUNT:objectAdmin" "gs://$BUCKET_NAME"
