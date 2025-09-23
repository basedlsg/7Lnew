# 7L / Impossible Tower

**Short take**: it’s a good seed, not a launchpad—folders match your "Impossible Tower" plan, but it’s missing the glue and docs you’ll need to actually run 7L autonomously on GCP.

## What’s promising
- **Structure**: top-level , , and  separate task logic, training, and documentation.
- **Languages**: mostly Python with Shell/HTML/Mermaid — fits services + infra + diagrams.
- **Cloud artifacts**:  and pointers to large files show GCS planning without bloating the repo.

## Gaps blocking progress
- **No runnable path end-to-end**: Missing Terraform, full Cloud Build YAMLs, and a Vertex Pipeline to reproduce the Cloud Run + Scheduler loop.
- **Missing service contracts**: MCP/HTTP for ,  (proxy), and  not checked in (OpenAPI or FastAPI stubs).
- **No program schema + checker tests**: Need a frozen  and unit/property tests (sat/unsat, edge geometry, friction=0, reverse gravity).
- **Docs are thin**:  doesn’t expose quickstart, env vars, or one-click Cloud Shell path.
- **Model path unclear**:  lacks training/eval scripts or Vertex Job spec.

## Concrete, high-leverage fixes
See  for actionable checklists. TL;DR:
- Repo hygiene & docs: Quickstart, ARCH, CONTRACTS, gold examples.
- Infra as code: minimal Terraform + Cloud Build.
- Service stubs: , , .
- Runner + Scheduler:  with GCS/BQ and logging.
- Test data:  with 4 tiny scenes.

## Quickstart (planned)
When implemented, Cloud Shell one-liner:

This will build → deploy → schedule → smoke-test.

## Status
- This README and docs outline the plan only; app code remains unchanged.
