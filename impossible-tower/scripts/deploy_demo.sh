#!/usr/bin/env bash
set -euo pipefail

if [ -z "${GCP_PROJECT:-}" ]; then
  echo "GCP_PROJECT is not set" >&2
  exit 1
fi

SERVICE_NAME="impossible-tower-demo"
REGION=${REGION:-us-central1}
IMAGE="gcr.io/$GCP_PROJECT/$SERVICE_NAME:latest"

cat <<MSG
Building demo container and deploying to Cloud Run.
Ensure CHECKER_SERVICE_URL, VERTEX_ENDPOINT_URL secrets are configured in Cloud Run.
MSG

# gcloud builds submit --tag "$IMAGE" --project "$GCP_PROJECT" --config cloudbuild-demo.yaml
# gcloud run deploy "$SERVICE_NAME" \
#   --image "$IMAGE" \
#   --project "$GCP_PROJECT" \
#   --platform managed \
#   --region "$REGION" \
#   --allow-unauthenticated \
#   --set-env-vars CHECKER_SERVICE_URL="$CHECKER_SERVICE_URL",VERTEX_ENDPOINT_URL="$VERTEX_ENDPOINT_URL"
