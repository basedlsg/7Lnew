# Secrets Management

> Do not commit secrets to the repository. Use this guide to provision runtime credentials safely.

## Required secrets

| Name | Description | Suggested storage |
| ---- | ----------- | ----------------- |
| `VERTEX_PROJECT_ID` | GCP project containing Vertex AI resources | `.env` (local), Secret Manager (prod) |
| `VERTEX_LOCATION` | Region for Vertex AI endpoints/jobs | `.env` |
| `VERTEX_ENDPOINT_ID` | Deployed endpoint ID for the multimodal model | `.env` |
| `VERTEX_ENDPOINT_URL` | Full REST endpoint URL | `.env` |
| `USE_VERTEX_PUBLISHER_MODEL` | Toggle to call Vertex publisher models (e.g., Gemini) instead of a private endpoint | `.env` |
| `VERTEX_PUBLISHER_MODEL` | Publisher model name (`gemini-1.5-flash`, etc.) | `.env` |
| `VERTEX_TEMPERATURE` | Generation temperature for publisher models | `.env` |
| `VERTEX_MAX_OUTPUT_TOKENS` | Token cap for publisher model responses | `.env` |
| `GCP_SERVICE_ACCOUNT_KEY_PATH` | Path to service account JSON key (if using key-based auth) | Keep outside repo, reference via env var |
| `GCS_DATA_BUCKET` | Bucket used for datasets and artifacts | `.env` |
| Optional: `OPENAI_API_KEY` | Only if auxiliary OpenAI APIs are used | Secret store, never committed |

## Local development

1. Copy `.env.example` to `.env`.
2. Populate values with placeholders or actual credentials. Avoid reusing production credentials for local work.
3. Export environment variables when running scripts:

   ```bash
   export $(grep -v '^#' .env | xargs)
   ```

## Codex Cloud usage

If using Codex Cloud, store secrets in the agent secret store as described in the Codex best practices documentation. Reference them at runtime via environment variables; do not hardcode them in source files.

## Deployment

- Prefer workload identity or service account impersonation instead of long-lived keys.
- For GitHub Actions, use `secrets.*` variables and never echo the values.
- Rotate keys regularly and audit access to GCS buckets and Vertex endpoints.

## Incident response

If a secret leaks:

1. Revoke the compromised credential immediately (disable key or endpoint access).
2. Rotate the secret and update all dependent services.
3. Open an issue documenting the incident and mitigation steps.

## Cloud Run secrets

- Set `CHECKER_SERVICE_URL` and `VERTEX_ENDPOINT_URL` via `gcloud run services update`.
- Use Secret Manager for service account keys (bind with IAM).
