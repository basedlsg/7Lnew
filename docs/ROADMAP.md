# Roadmap and Actionable Checklists

Keep changes git-only; do not modify service code until stubs are scaffolded.

## Repo hygiene & docs
- [ ] Root quickstart ()
- [ ]  (Mermaid)
- [ ]  (HTTP schemas + examples)
- [ ]  + 10 gold examples (possible/impossible)
- [ ]  quickstart and env var reference

## Infra as Code (minimum viable)
- [ ]  (GCS, BQ, Artifact Registry, Cloud Run x4, Scheduler)
- [ ]  per-service  + root orchestrator
- [ ] Vertex Pipeline/CustomJob spec for training/eval

## Service stubs
- [ ]  POST /analyze (canned scene_graph)
- [ ]  POST /check (runs Z3; unit tests)
- [ ]  POST /infer (heuristic fallback w/o creds)

## Runner + Scheduler
- [ ]  orchestrates queue → services → writes runs/*.jsonl → BQ
- [ ] Idempotency + Cloud Logging

## Test data
- [ ]  A–D scenes (<200KB PNGs) + scene_graphs

## CI / DX
- [ ] GitHub Actions: lint, unit tests, container build (dry-run)
- [ ] Data/Model cards populated with commit SHA + run IDs
- [ ]  examples calling services via HTTP
