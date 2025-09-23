# Model Card

## Model details

- **Model family:** Vertex AI-hosted multimodal model (e.g., PaliGemma, Gemma-based LLaVA)
- **Task:** Program-of-thought generation describing physical constraints
- **Input:** Multi-view images (GCS URIs), optional scene metadata, natural language prompt
- **Output:** Structured JSON program with assumptions and claims, plus natural-language rationale
- **Status:** Fine-tuning pipeline scaffolded; users must deploy with their Vertex project settings

## Intended use

- Detect physically impossible scenes and produce symbolic proof artifacts
- Research experiments combining neural perception with symbolic solvers

## Factors

- **Data:** Synthetic PyBullet scenes (see `docs/data-card.md`)
- **Compute:** Vertex AI Custom Jobs and Endpoints
- **Metrics:** Accuracy@1, Z3 pass rate, violation rate, counterexample rate, cross-view consistency

## Evaluation

- Evaluation harness (`src/model/train_vertex/eval.py`) runs on validation splits from synthetic data
- Results summarized in `docs/evals.md`

## Ethical considerations

- Generated proofs may leak scene metadata; avoid ingesting sensitive imagery
- Provide content moderation if deploying a public API (see safety note below)

## Safety

- Integrate with Google Cloud Content Safety or OpenAI moderation for user-provided images
- Log solver traces without user PII; redact GCS URIs before sharing externally

## Caveats

- Model relies on Vertex-managed infrastructure; users must secure endpoints and costs
- No guarantee of robust generalization to real-world photographs

### Deployment options

- **Private endpoint**: Deploy fine-tuned adapters to a custom Vertex endpoint and set `VERTEX_ENDPOINT_URL`.
- **Publisher model**: Set `USE_VERTEX_PUBLISHER_MODEL=true` and choose `VERTEX_PUBLISHER_MODEL` (e.g., `gemini-1.5-flash`) to call Google-hosted Gemini models through the publisher API.

## Demo inference

- Demo Cloud Run URL: https://impossible-tower-demo-612990030705.us-central1.run.app
- Checker Cloud Run URL: https://impossible-tower-checker-612990030705.us-central1.run.app
