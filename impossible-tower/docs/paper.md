# The Impossible Tower: Neural-Symbolic Proofs of Physical Impossibility

## Abstract

We introduce Impossible Tower, a reproducible benchmark and system for detecting and explaining physically impossible scenes using hybrid neural-symbolic reasoning. Synthetic multi-view renders are paired with symbolic constraints, enabling multimodal large language models to emit structured proof programs that are then validated by a Z3 checker.

## 1. Introduction

Perception systems remain brittle when confronted with violations of common-sense physics. Impossible Tower proposes a data-to-deployment pipeline that blends PyBullet-based simulation, Vertex AI-hosted multimodal models, and SMT-based verification to produce verifiable proofs of impossibility.

## 2. Method

- **Data generation:** Seeded PyBullet simulations produce both feasible and infeasible stacks, exporting images, scene graphs, and constraint sets. A Cloud Run Job now refreshes the dataset daily to `gs://impossible-tower-data/itower/<date>/` for continual evaluation.
- **Program-of-thought model:** A Vertex fine-tuned model consumes multi-view imagery and emits symbolic assumptions and claims. The production client can also call Gemini (`publishers/google/models/gemini-1.5-flash`) via the Vertex publisher API for rapid bootstrapping.
- **Symbolic checker:** A FastAPI microservice wraps Z3 constraints enforcing support, contact, and stability.
- **Demo & tooling:** A FastAPI demo orchestrates model inference and proof validation, serving human-readable explanations and counterexamples.

## 3. Experiments

Planned experiments evaluate the model on synthetic validation splits, reporting Accuracy@1, Program Pass Rate, Violation Rate, Counterexample Rate, and Cross-view Consistency. Early baselines rely on zero-shot Vertex models; future work fine-tunes via LoRA.

## 4. Results

| Setup | Acc@1 | Pass | Violations | CE Rate |
| ----- | ----- | ---- | ---------- | ------- |
| Baseline (mock program) | 0.500 | 0.000 | 4.000 | 1.000 |

## 5. Limitations & Future Work

- Low visual fidelity; requires domain randomization for real-world transfer.
- Simplified physics approximations (AABB collisions, friction cone).
- Reliance on cloud-hosted models introduces cost and latency considerations.

Future directions include photoreal renderers, hard-negative mining from real images, and a human-readable proof DSL.

## References

(*Add citations in subsequent iterations.*)
