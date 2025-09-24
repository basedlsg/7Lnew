#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID=${PROJECT_ID:-""}
LOCATION=${LOCATION:-"us-central1"}
BUCKET=${BUCKET:-"impossible-tower-data"}

if [[ -z "$PROJECT_ID" ]]; then echo "Set PROJECT_ID env var"; exit 1; fi

echo "Enabling APIs..."
gcloud services enable aiplatform.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --project "$PROJECT_ID"

echo "Creating Artifact Registry repo if missing..."
gcloud artifacts repositories create itower --repository-format=DOCKER --location="$LOCATION" --project "$PROJECT_ID" || true

echo "Creating bucket if missing..."
gsutil mb -p "$PROJECT_ID" -l "$LOCATION" "gs://$BUCKET" || true

echo "Building and deploying services..."
for svc in scene-service vertex-proxy z3-checker itower-runner; do
  (cd services/$svc && gcloud builds submit --config cloudbuild.yaml --project "$PROJECT_ID" --substitutions _LOCATION="$LOCATION")
done

echo "Smoke test runner..."
RUN_URL=$(gcloud run services describe itower-runner --region "$LOCATION" --project "$PROJECT_ID" --format='value(status.url)')
curl -s -X POST "$RUN_URL/run" | jq . || echo '{}'
