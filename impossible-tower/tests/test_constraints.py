from data_gen.constraints import constraints_from_scene
from data_gen.pybullet_worlds import BlockSpec, ObjectState, SceneSample


def test_constraints_include_com_within_support():
    block0 = BlockSpec(name="block_0", half_extents=(0.2, 0.2, 0.1), mass=2.0)
    block1 = BlockSpec(name="block_1", half_extents=(0.1, 0.1, 0.1), mass=1.0)
    obj0 = ObjectState(
        name="block_0",
        block=block0,
        position=(0.0, 0.0, 0.1),
        orientation=(0.0, 0.0, 0.0, 1.0),
        linear_velocity=(0.0, 0.0, 0.0),
        angular_velocity=(0.0, 0.0, 0.0),
        aabb_min=(-0.2, -0.2, 0.0),
        aabb_max=(0.2, 0.2, 0.2),
    )
    obj1 = ObjectState(
        name="block_1",
        block=block1,
        position=(0.0, 0.0, 0.3),
        orientation=(0.0, 0.0, 0.0, 1.0),
        linear_velocity=(0.0, 0.0, 0.0),
        angular_velocity=(0.0, 0.0, 0.0),
        aabb_min=(-0.1, -0.1, 0.2),
        aabb_max=(0.1, 0.1, 0.4),
    )
    contacts = [
        {
            "body_a": "block_1",
            "body_b": "block_0",
            "position_on_a": (0.0, 0.0, 0.2),
            "position_on_b": (0.0, 0.0, 0.2),
            "normal": (0.0, 0.0, 1.0),
            "normal_force": 9.8,
        }
    ]
    sample = SceneSample(objects=[obj0, obj1], contacts=contacts, stable=True, seed=456)
    constraints = constraints_from_scene(sample)
    assert "com_within_support(block_1)" in constraints["assumptions"]
