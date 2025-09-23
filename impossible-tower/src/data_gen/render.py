"""Rendering helpers for Impossible Tower scenes."""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, MutableMapping, Tuple

import numpy as np
import pybullet as p
from PIL import Image

from .pybullet_worlds import BlockSpec, SceneSample, configure_pybullet, spawn_block


Vec3 = Tuple[float, float, float]


@dataclass
class CameraPose:
    position: Vec3
    target: Vec3
    up: Vec3 = (0.0, 0.0, 1.0)


@dataclass
class RenderConfig:
    width: int = 320
    height: int = 320
    fov: float = 60.0
    near: float = 0.1
    far: float = 3.0
    camera_poses: Tuple[CameraPose, ...] = (
        CameraPose(position=(0.6, 0.0, 0.4), target=(0.0, 0.0, 0.2)),
        CameraPose(position=(0.0, 0.6, 0.4), target=(0.0, 0.0, 0.2)),
        CameraPose(position=(-0.6, 0.0, 0.4), target=(0.0, 0.0, 0.2)),
        CameraPose(position=(0.0, -0.6, 0.4), target=(0.0, 0.0, 0.2)),
    )


def _respawn_static_scene(scene: SceneSample) -> Tuple[int, Mapping[str, int]]:
    client = configure_pybullet(gui=False)
    body_ids: Dict[str, int] = {}
    for obj in scene.objects:
        pose = (obj.position, obj.orientation)
        body_ids[obj.name] = spawn_block(obj.block, pose, client)
        p.resetBaseVelocity(body_ids[obj.name], linearVelocity=(0, 0, 0), angularVelocity=(0, 0, 0), physicsClientId=client)
        p.resetBasePositionAndOrientation(body_ids[obj.name], obj.position, obj.orientation, physicsClientId=client)
    return client, body_ids


def render_views(scene: SceneSample, config: RenderConfig | None = None) -> Dict[str, np.ndarray]:
    cfg = config or RenderConfig()
    client, body_lookup = _respawn_static_scene(scene)
    width, height = cfg.width, cfg.height
    aspect = width / height
    results: Dict[str, np.ndarray] = {}

    for idx, pose in enumerate(cfg.camera_poses):
        view_matrix = p.computeViewMatrix(cameraEyePosition=pose.position, cameraTargetPosition=pose.target, cameraUpVector=pose.up)
        proj_matrix = p.computeProjectionMatrixFOV(fov=cfg.fov, aspect=aspect, nearVal=cfg.near, farVal=cfg.far)
        image = p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=view_matrix,
            projectionMatrix=proj_matrix,
            shadow=1,
            lightDirection=[1, 1, 1],
            physicsClientId=client,
        )
        rgba = np.reshape(image[2], (height, width, 4))
        cam_id = f"cam_{idx:02d}"
        results[cam_id] = rgba[:, :, :3].astype(np.uint8)

    p.disconnect(client)
    return results


def save_views(images: Mapping[str, np.ndarray], output_dir: pathlib.Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for cam_id, array in images.items():
        path = output_dir / f"{cam_id}.png"
        Image.fromarray(array).save(path)


def save_camera_config(config: RenderConfig, output_dir: pathlib.Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cameras = []
    for idx, pose in enumerate(config.camera_poses):
        cameras.append(
            {
                "camera_id": f"cam_{idx:02d}",
                "position": pose.position,
                "target": pose.target,
                "up": pose.up,
                "fov": config.fov,
                "near": config.near,
                "far": config.far,
            }
        )
    (output_dir / "cameras.json").write_text(json.dumps(cameras, indent=2))
