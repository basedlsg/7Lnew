#!/usr/bin/env bash
set -euo pipefail

if [ -z "${GCP_PROJECT:-}" ]; then
  echo "GCP_PROJECT is not set" >&2
  exit 1
fi

SERVICE_NAME="impossible-tower-checker"
REGION=${REGION:-us-central1}
IMAGE="gcr.io/$GCP_PROJECT/$SERVICE_NAME:latest"

cat <<MSG
Building checker container and deploying to Cloud Run.
You may need Artifact Registry permissions.
MSG

# gcloud builds submit --tag "$IMAGE" --project "$GCP_PROJECT"
# gcloud run deploy "$SERVICE_NAME" \
#   --image "$IMAGE" \
#   --project "$GCP_PROJECT" \
#   --platform managed \
#   --region "$REGION" \
#   --allow-unauthenticated
