# Impossible Tower

Impossible Tower is a reproducible research stack for detecting physically impossible scenes and producing symbolic proofs of the violations. Synthetic PyBullet scenes feed a Vertex AI-accessible multimodal model that emits structured proof programs, which are then validated by a Z3 microservice. A FastAPI demo orchestrates the workflow and publishes the verdict plus proof artifacts.

## Cloud deployment snapshot (2025-09-19)
- **Dataset**: `gs://impossible-tower-data/itower/v0.1/synth_500` (500 labelled scenes with renders, scene graphs, constraints)
- **Checker**: Cloud Run → `https://impossible-tower-checker-612990030705.us-central1.run.app`
- **Demo**: Cloud Run → `https://impossible-tower-demo-612990030705.us-central1.run.app`
- **Autogen**: Cloud Run Job `itower-datagenerator` + Scheduler `itower-daily-generator` drops 500 new scenes daily to `gs://impossible-tower-data/itower/<date>/synth_500`
- **Model**: Demo currently calls Gemini (`publishers/google/models/gemini-1.5-flash`) via Vertex publisher API for structured program output

## Getting started

1. Clone the repository and create a virtual environment.
2. Install dependencies: `pip install -e .[dev]`.
3. Generate a smoke dataset with `bash scripts/synth_100.sh --local` (writes to `data/synth_50`).
4. Review deployment + API details in `docs/getting-started.md` and `docs/api.md`.

## Development tasks

- `pytest` — unit tests for data, checker, Vertex client
- `bash scripts/run_eval.sh small` — evaluation harness producing Markdown metrics
- `gcloud run jobs execute itower-datagenerator --region us-central1` — manual trigger of the daily dataset job
- `uvicorn src.checker.service:app --reload --port 8081` — local checker
- `uvicorn src.demo.app:app --reload --port 8080` — local demo (requires checker running)

## Contributing

Please use pre-commit hooks and open PRs against `main`. See `docs/milestones.md` for the active task list and status.

## License

MIT License — see `LICENSE`.
