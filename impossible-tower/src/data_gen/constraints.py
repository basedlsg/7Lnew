"""Derive symbolic constraints for a scene."""

from __future__ import annotations

import json
import pathlib
from typing import Dict, List, Tuple


from .scene_graph import scene_graph
from .pybullet_worlds import SceneSample


Vec2 = Tuple[float, float]


def _project_to_support_polygon(com_xy: Vec2, polygon: List[Vec2]) -> bool:
    xs, ys = zip(*polygon)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return min_x <= com_xy[0] <= max_x and min_y <= com_xy[1] <= max_y


def _support_relationships(scene: SceneSample) -> Dict[str, List[str]]:
    supports: Dict[str, List[str]] = {}
    for contact in scene.contacts:
        normal = contact["normal"]
        if normal[2] > 0.5:
            supports.setdefault(contact["body_a"], []).append(contact["body_b"])
    return supports


def constraints_from_scene(scene: SceneSample) -> Dict[str, object]:
    graph = scene_graph(scene)
    supports = _support_relationships(scene)

    com_constraints: Dict[str, Dict[str, object]] = {}
    for obj in graph["objects"]:
        supporters = supports.get(obj["name"], [])
        proj = (obj["com"][0], obj["com"][1])
        polygons = []
        for support_name in supporters:
            support_obj = next(o for o in graph["objects"] if o["name"] == support_name)
            polygons.append(support_obj["support_polygon_xy"])
        if polygons:
            within_all = all(_project_to_support_polygon(proj, poly) for poly in polygons)
        else:
            within_all = False
        com_constraints[obj["name"]] = {
            "com_xy": proj,
            "supporters": supporters,
            "within_support": within_all,
            "support_polygons": polygons,
        }

    assumptions: List[str] = []
    for contact in scene.contacts:
        assumptions.append(f"contact({contact['body_a']},{contact['body_b']})")
    for obj, supporters in supports.items():
        for supporter in supporters:
            assumptions.append(f"support({obj},{supporter})")
    for obj, info in com_constraints.items():
        if info["supporters"]:
            assumptions.append(f"com_within_support({obj})")

    claims = ["stable(scene)" if scene.stable else "unstable(scene)"]

    return {
        "assumptions": sorted(set(assumptions)),
        "claims": claims,
        "com_constraints": com_constraints,
        "supports": supports,
        "label": {"possible": scene.stable},
    }


def write_constraints(scene: SceneSample, output_path: pathlib.Path) -> None:
    data = constraints_from_scene(scene)
    output_path.write_text(json.dumps(data, indent=2))
