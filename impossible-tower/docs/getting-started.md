# Getting Started

This guide covers the minimum steps required to reproduce and operate Impossible Tower locally or on Google Cloud.

## Prerequisites

- Python 3.11+
- macOS build tip: if `pybullet` fails to compile due to `fdopen` macro, export `CFLAGS="-Dfdopen=fdopen"` before running `pip install -e .[dev]`.
- Google Cloud SDK (`gcloud`), duly authenticated (`gcloud auth application-default login`)
- Access to project **day-planner-london-mvp** (or another Vertex-enabled project)
- Cloud Storage bucket for datasets (created: `gs://impossible-tower-data`)
- Docker (for local container builds)
- PyBullet system dependencies (`xvfb`, `ffmpeg`) for local rendering

## Environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

Populate `.env` with your project settings. To use the live demo/checker, export:

```bash
export CHECKER_SERVICE_URL=https://impossible-tower-checker-612990030705.us-central1.run.app/check
export DEMO_SERVICE_URL=https://impossible-tower-demo-612990030705.us-central1.run.app
```

## Synthetic dataset

Generate a smoke dataset locally:

```bash
bash scripts/synth_100.sh --local
```

Generate a production split directly to GCS (already published at `gs://impossible-tower-data/itower/v0.1/synth_500`):

```bash
python -m data_gen.make_dataset \
  --out gs://impossible-tower-data/itower/v0.1/synth_500 \
  --n-scenes 500 --pos-frac 0.5 --views 4 --seed 7
```

## Services

Local development

```bash
uvicorn src.checker.service:app --reload --port 8081
uvicorn src.demo.app:app --reload --port 8080
```

Cloud Run (already deployed)

- Checker: `https://impossible-tower-checker-612990030705.us-central1.run.app`
- Demo: `https://impossible-tower-demo-612990030705.us-central1.run.app`

See `scripts/deploy_checker.sh` and `scripts/deploy_demo.sh` or run:

```bash
GCP_PROJECT=day-planner-london-mvp gcloud builds submit --config cloudbuild-checker.yaml
GCP_PROJECT=day-planner-london-mvp gcloud run deploy impossible-tower-checker ...
```

## Automated generation

- A Cloud Run Job (`itower-datagenerator`) creates 500-scene drops in `gs://impossible-tower-data/itower/<date>/synth_500`.
- Cloud Scheduler job (`itower-daily-generator`) invokes the Run Job every day at 02:00 UTC. Inspect via `gcloud scheduler jobs describe itower-daily-generator --location us-central1`.
- Run manually with `gcloud run jobs execute itower-datagenerator --region us-central1`.

## Eval harness

```bash
bash scripts/run_eval.sh small
```

The script writes Markdown tables to `docs/eval_results/` (e.g., `eval-20250919-121706.md`).

## Vertex / Gemini model

- Option A (custom endpoint): configure `VERTEX_ENDPOINT_URL` once you deploy a model fine-tune to Vertex AI; update Cloud Run demo with the env var.
- Option B (publisher model): set `USE_VERTEX_PUBLISHER_MODEL=true` and `VERTEX_PUBLISHER_MODEL=gemini-1.5-flash` (current production default). The client will call the Vertex publisher REST endpoint using ADC.
- Control generation behaviour via `VERTEX_TEMPERATURE` and `VERTEX_MAX_OUTPUT_TOKENS`.
