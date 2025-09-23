"""Scene graph export utilities."""

from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, List, Tuple

import numpy as np

from .pybullet_worlds import ObjectState, SceneSample


Vec3 = Tuple[float, float, float]


def _support_polygon_xy(obj: ObjectState) -> List[Tuple[float, float]]:
    hx, hy, _ = obj.block.half_extents
    cx, cy, _ = obj.position
    return [
        (cx - hx, cy - hy),
        (cx + hx, cy - hy),
        (cx + hx, cy + hy),
        (cx - hx, cy + hy),
    ]


def _quat_to_euler(quat: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
    x, y, z, w = quat
    # Standard quaternion to Euler (xyz order) conversion.
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    return roll, pitch, yaw


def scene_graph(scene: SceneSample) -> Dict[str, object]:
    objects: List[Dict[str, object]] = []
    for obj in scene.objects:
        objects.append(
            {
                "name": obj.name,
                "mass": obj.block.mass,
                "half_extents": obj.block.half_extents,
                "position": obj.position,
                "orientation_quat": obj.orientation,
                "orientation_euler": _quat_to_euler(obj.orientation),
                "linear_velocity": obj.linear_velocity,
                "angular_velocity": obj.angular_velocity,
                "aabb": {
                    "min": obj.aabb_min,
                    "max": obj.aabb_max,
                },
                "support_polygon_xy": _support_polygon_xy(obj),
                "com": obj.position,
            }
        )

    contacts = [
        {
            "body_a": c["body_a"],
            "body_b": c["body_b"],
            "normal": c["normal"],
            "normal_force": c["normal_force"],
            "position_on_a": c["position_on_a"],
            "position_on_b": c["position_on_b"],
        }
        for c in scene.contacts
    ]

    adjacency: Dict[str, List[str]] = {}
    for contact in contacts:
        adjacency.setdefault(contact["body_a"], []).append(contact["body_b"])
        adjacency.setdefault(contact["body_b"], []).append(contact["body_a"])

    return {
        "seed": scene.seed,
        "stable": scene.stable,
        "objects": objects,
        "contacts": contacts,
        "adjacency": adjacency,
        "gravity": [0.0, 0.0, -9.81],
    }


def write_scene_graph(scene: SceneSample, output_path: pathlib.Path) -> None:
    data = scene_graph(scene)
    output_path.write_text(json.dumps(data, indent=2))
