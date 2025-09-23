# Milestone Tracking

## M1: Repository scaffolding
- [x] Layout repo, linting, CI, docs
- [x] Provide secrets workflow and env templates

## M2: Data generation + schemas
- [x] Implement PyBullet scene generator
- [x] Provide dataset CLI exporting to GCS
- [x] Generate ≥500-scene dataset to `gs://impossible-tower-data/itower/v0.1/synth_500`

## M3: Model + checker plumbing
- [x] Stub Vertex client with mock fallback
- [x] Provide Vertex training pipeline skeleton
- [x] Implement Z3 checker service + tests

## M4: Demo + evaluation
- [x] FastAPI demo + UI calling model and checker
- [x] Evaluation harness writes Markdown metrics
- [x] CI configured with lint/tests/nightly eval matrix

-## M5: Cloud deployment
- [x] Build and push checker Cloud Run service
- [x] Build and push demo Cloud Run service
- [x] Schedule automated dataset generation (Cloud Run Job + Scheduler)
- [ ] Configure Vertex endpoint + secrets in Cloud Run (pending live model wiring)
