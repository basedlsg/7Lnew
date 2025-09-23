"""CLI for generating Impossible Tower datasets."""

from __future__ import annotations

import json
import pathlib
import numpy as np
import tempfile
from typing import Optional

import typer
from google.cloud import storage

from .constraints import constraints_from_scene, write_constraints
from .pybullet_worlds import SceneSample, generate_scene
from .render import RenderConfig, render_views, save_camera_config, save_views
from .scene_graph import scene_graph, write_scene_graph


app = typer.Typer(add_completion=False)


def _is_gcs_path(path: str) -> bool:
    return path.startswith("gs://")



def _upload_directory(local_dir: pathlib.Path, gcs_uri: str) -> None:
    if not _is_gcs_path(gcs_uri):
        raise ValueError("gcs_uri must start with gs://")
    bucket_name, _, prefix = gcs_uri[5:].partition("/")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    for path in local_dir.rglob("*"):
        if path.is_dir():
            continue
        dest_path = f"{prefix}/{path.relative_to(local_dir)}".strip("/")
        blob = bucket.blob(dest_path)
        blob.upload_from_filename(path.as_posix())


def _write_sample(  # type: ignore[override]
    sample_dir: pathlib.Path,
    scene: SceneSample,
    render_cfg: RenderConfig,
) -> None:
    images = render_views(scene, render_cfg)
    save_views(images, sample_dir / "images")
    save_camera_config(render_cfg, sample_dir)
    write_scene_graph(scene, sample_dir / "scene_graph.json")
    write_constraints(scene, sample_dir / "constraints.json")
    (sample_dir / "label.json").write_text(json.dumps({"possible": scene.stable}, indent=2))


@app.command()
def main(
    out: str = typer.Option(..., help="Output directory (local path or gs:// bucket)"),
    n_scenes: int = typer.Option(100, help="Number of scenes to generate"),
    pos_frac: float = typer.Option(0.5, help="Fraction of scenes that are physically possible"),
    views: int = typer.Option(4, help="Number of camera views"),
    seed: int = typer.Option(0, help="Random seed"),
) -> None:
    default_cfg = RenderConfig()
    if views > len(default_cfg.camera_poses):
        raise typer.BadParameter(f"views must be <= {len(default_cfg.camera_poses)}")
    render_cfg = RenderConfig(camera_poses=default_cfg.camera_poses[:views])
    base_path = pathlib.Path(out)
    use_gcs = _is_gcs_path(out)

    rng = np.random.default_rng(seed)
    if use_gcs:
        tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="itower_"))
    else:
        base_path.mkdir(parents=True, exist_ok=True)
        tmp_dir = base_path

    for idx in range(n_scenes):
        scene_seed = seed + idx
        should_be_stable = rng.random() < pos_frac
        scene = generate_scene(seed=scene_seed, stable=should_be_stable)
        sample_dir = tmp_dir / f"scene_{idx:05d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        _write_sample(sample_dir, scene, render_cfg)

    rng = np.random.default_rng(seed)
    if use_gcs:
        _upload_directory(tmp_dir, out)
        typer.echo(f"Uploaded dataset to {out}")
    else:
        typer.echo(f"Dataset available at {base_path}")


if __name__ == "__main__":
    app()
