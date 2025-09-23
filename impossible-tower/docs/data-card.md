# Data Card

## Overview

- **Name:** Impossible Tower Synthetic Scenes
- **Version:** 0.1
- **Creators:** Impossible Tower contributors
- **License:** MIT (code), CC-BY (generated media)

## Motivation

The dataset captures synthetic stacks of rigid bodies under gravity. Half of the scenes satisfy Newtonian stability constraints; the other half violate them (e.g., unsupported mass, interpenetration, inverted gravity). Each scene includes geometry, physics metadata, and symbolic constraint annotations to support proof generation and automated verification.

## Distribution

- Location: `gs://impossible-tower-data/itower/v0.1/`
- Daily autogen: `gs://impossible-tower-data/itower/<YYYY-MM-DD>/synth_500`
- Versioning: directories per release (e.g., `synth_500`)

## Composition

- Multi-view PNG renders (TinyRenderer via PyBullet)
- Camera intrinsics/extrinsics (`cameras.json`)
- Scene graph with poses, AABBs, contact map (`scene_graph.json`)
- Constraint set (`constraints.json`) capturing support, stability, and collision rules
- Ground-truth label (`label.json`)
- Optional stitched video (`video.mp4`)

## Collection process

Scenes are generated procedurally using seeded random sampling. PyBullet simulates rigid body dynamics under standard gravity until convergence or instability. Impossible scenes are created by injecting constraint-breaking perturbations.

## Recommended uses

- Training multimodal models to reason about physical plausibility
- Benchmarking symbolic reasoning pipelines
- Research exploring hybrid neural-symbolic systems

## Limitations

- Low visual fidelity; TinyRenderer outputs may not match real-world textures
- Only simple block-like geometries initially
- Physics approximations (AABB collision, simplified friction cone)

## Maintenance

- Versioning via GCS paths (e.g., `gs://<bucket>/itower/v0.1/...`)
- Regeneration is deterministic given seeds documented in metadata
- Future updates will expand object catalogs and photorealistic renders
