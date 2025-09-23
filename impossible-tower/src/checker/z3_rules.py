"""Z3-based validation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, MutableMapping

import z3


@dataclass
class Violation:
    rule: str
    subject: str
    details: Mapping[str, object]

    def as_dict(self) -> Dict[str, object]:
        return {"rule": self.rule, "subject": self.subject, "details": dict(self.details)}


def _rect_contains(point: List[float], polygon: List[List[float]]) -> bool:
    xs = [v[0] for v in polygon]
    ys = [v[1] for v in polygon]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    solver = z3.Solver()
    x = z3.Real("x")
    y = z3.Real("y")
    solver.add(x == point[0])
    solver.add(y == point[1])
    solver.add(x >= min_x, x <= max_x)
    solver.add(y >= min_y, y <= max_y)
    return solver.check() == z3.sat


def _contact_lookup(scene_graph: Mapping[str, object]) -> Mapping[str, List[str]]:
    contacts = scene_graph.get("contacts", [])
    mapping: MutableMapping[str, List[str]] = {}
    for contact in contacts:
        a, b = contact["body_a"], contact["body_b"]
        mapping.setdefault(a, []).append(b)
        mapping.setdefault(b, []).append(a)
    return mapping


def validate_program(
    program: Mapping[str, object],
    scene_graph: Mapping[str, object],
    constraints: Mapping[str, object] | None = None,
) -> Dict[str, object]:
    constraints = constraints or {}
    violations: List[Violation] = []
    contact_map = _contact_lookup(scene_graph)
    assumptions = program.get("assumptions", [])

    for assumption in assumptions:
        if assumption.startswith("contact("):
            body_a, body_b = assumption[len("contact(") : -1].split(",")
            if body_b not in contact_map.get(body_a, []):
                violations.append(Violation("contact", body_a, {"expected_contact": body_b}))
        elif assumption.startswith("support("):
            body_a, body_b = assumption[len("support(") : -1].split(",")
            if body_b not in contact_map.get(body_a, []):
                violations.append(Violation("support_contact", body_a, {"supporter": body_b}))
        elif assumption.startswith("com_within_support("):
            target = assumption[len("com_within_support(") : -1]
            com_constraints = constraints.get("com_constraints", {})
            info = com_constraints.get(target)
            if not info:
                violations.append(Violation("com_missing", target, {}))
                continue
            supporters = info.get("supporters", [])
            if not supporters:
                violations.append(Violation("com_no_support", target, {}))
                continue
            polygons = info.get("support_polygons", [])
            if not polygons:
                violations.append(Violation("support_polygon_missing", target, {}))
                continue
            com_xy = info.get("com_xy", [0.0, 0.0])
            if not all(_rect_contains(com_xy, poly) for poly in polygons):
                violations.append(
                    Violation(
                        "com_support",
                        target,
                        {
                            "com_xy": com_xy,
                            "support_polygons": polygons,
                        },
                    )
                )

    is_pass = not violations
    counterexample = {}
    if violations:
        first = violations[0]
        counterexample = first.details

    return {
        "pass": is_pass,
        "violations": [v.as_dict() for v in violations],
        "counterexample": counterexample,
    }
