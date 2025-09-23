"""Utilities for constructing PyBullet tower scenes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pybullet as p
import pybullet_data


Vec3 = Tuple[float, float, float]
Quat = Tuple[float, float, float, float]


@dataclass
class BlockSpec:
    name: str
    half_extents: Vec3
    mass: float


@dataclass
class ObjectState:
    name: str
    block: BlockSpec
    position: Vec3
    orientation: Quat
    linear_velocity: Vec3
    angular_velocity: Vec3
    aabb_min: Vec3
    aabb_max: Vec3


@dataclass
class SceneSample:
    objects: List[ObjectState]
    contacts: List[Dict[str, object]]
    stable: bool
    seed: int


DEFAULT_FRICTION = 0.8
DEFAULT_RESTITUTION = 0.0
GRAVITY = -9.81


def configure_pybullet(gui: bool = False, seed: Optional[int] = None) -> int:
    client = p.connect(p.GUI if gui else p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=client)
    p.resetSimulation(physicsClientId=client)
    p.setGravity(0, 0, GRAVITY, physicsClientId=client)
    p.setTimeStep(1.0 / 240.0, physicsClientId=client)
    if seed is not None:
        np.random.seed(seed)
    plane_id = p.loadURDF("plane.urdf", physicsClientId=client)
    p.changeDynamics(plane_id, -1, lateralFriction=DEFAULT_FRICTION, restitution=DEFAULT_RESTITUTION)
    return client


def random_block_specs(num_blocks: int, rng: np.random.Generator) -> List[BlockSpec]:
    specs: List[BlockSpec] = []
    for i in range(num_blocks):
        half_extents = tuple(rng.uniform(0.05, 0.15, size=3))  # type: ignore[assignment]
        mass = float(rng.uniform(0.5, 2.0))
        specs.append(BlockSpec(name=f"block_{i}", half_extents=half_extents, mass=mass))
    return specs


def spawn_block(block: BlockSpec, pose: Tuple[Vec3, Quat], client: int) -> int:
    collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=block.half_extents, physicsClientId=client)
    visual = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=block.half_extents,
        rgbaColor=(0.6, 0.6, 0.9, 1.0),
        physicsClientId=client,
    )
    body_id = p.createMultiBody(
        baseMass=block.mass,
        baseCollisionShapeIndex=collision,
        baseVisualShapeIndex=visual,
        basePosition=pose[0],
        baseOrientation=pose[1],
        physicsClientId=client,
    )
    p.changeDynamics(
        body_id,
        -1,
        lateralFriction=DEFAULT_FRICTION,
        restitution=DEFAULT_RESTITUTION,
        physicsClientId=client,
    )
    return body_id


def settle_simulation(client: int, steps: int = 480) -> None:
    for _ in range(steps):
        p.stepSimulation(physicsClientId=client)


def _generate_stack_layout(
    specs: Sequence[BlockSpec],
    stable: bool,
    rng: np.random.Generator,
) -> List[Tuple[Vec3, Quat]]:
    poses: List[Tuple[Vec3, Quat]] = []
    base_x, base_y = 0.0, 0.0
    cumulative_height = 0.0
    for i, block in enumerate(specs):
        z = cumulative_height + block.half_extents[2]
        if stable:
            offset = rng.normal(loc=0.0, scale=0.01, size=2)
        else:
            if i == len(specs) - 1:
                offset = rng.normal(loc=0.16, scale=0.015, size=2)
            else:
                offset = rng.normal(loc=0.0, scale=0.025, size=2)
        pose = ((base_x + float(offset[0]), base_y + float(offset[1]), z), p.getQuaternionFromEuler((0, 0, 0)))
        poses.append(pose)
        cumulative_height = z + block.half_extents[2]
    if not stable and len(poses) >= 2:
        top_pos, top_quat = poses[-1]
        poses[-1] = ((top_pos[0], top_pos[1], top_pos[2] + 0.04), top_quat)
    return poses


def collect_contacts(client: int, id_to_name: Dict[int, str]) -> List[Dict[str, object]]:
    contacts: List[Dict[str, object]] = []
    ids = list(id_to_name.keys())
    for idx_a, body_a in enumerate(ids):
        for body_b in ids[idx_a + 1 :]:
            for cp in p.getContactPoints(bodyA=body_a, bodyB=body_b, physicsClientId=client):
                contacts.append(
                    {
                        "body_a": id_to_name[body_a],
                        "body_b": id_to_name[body_b],
                        "position_on_a": cp[5],
                        "position_on_b": cp[6],
                        "normal": cp[7],
                        "normal_force": cp[9],
                    }
                )
    return contacts


def generate_scene(seed: int, num_blocks: int = 4, stable: Optional[bool] = None, gui: bool = False) -> SceneSample:
    rng = np.random.default_rng(seed)
    is_stable = stable if stable is not None else bool(rng.integers(0, 2))
    client = configure_pybullet(gui=gui, seed=seed)
    specs = random_block_specs(num_blocks=num_blocks, rng=rng)
    poses = _generate_stack_layout(specs=specs, stable=is_stable, rng=rng)

    objects: List[ObjectState] = []
    id_to_name: Dict[int, str] = {}
    body_ids: List[int] = []

    for spec, pose in zip(specs, poses):
        body_id = spawn_block(spec, pose, client)
        id_to_name[body_id] = spec.name
        body_ids.append(body_id)

    settle_simulation(client)

    for spec, body_id in zip(specs, body_ids):
        pos, quat = p.getBasePositionAndOrientation(body_id, physicsClientId=client)
        lin_vel, ang_vel = p.getBaseVelocity(body_id, physicsClientId=client)
        aabb_min, aabb_max = p.getAABB(body_id, physicsClientId=client)
        objects.append(
            ObjectState(
                name=spec.name,
                block=spec,
                position=pos,
                orientation=quat,
                linear_velocity=lin_vel,
                angular_velocity=ang_vel,
                aabb_min=aabb_min,
                aabb_max=aabb_max,
            )
        )

    contacts = collect_contacts(client, id_to_name)
    p.disconnect(client)
    return SceneSample(objects=objects, contacts=contacts, stable=is_stable, seed=seed)
