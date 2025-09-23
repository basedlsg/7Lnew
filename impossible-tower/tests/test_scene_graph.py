from data_gen.pybullet_worlds import BlockSpec, ObjectState, SceneSample
from data_gen.scene_graph import scene_graph


def test_scene_graph_contains_objects():
    block = BlockSpec(name="block_0", half_extents=(0.1, 0.1, 0.1), mass=1.0)
    obj = ObjectState(
        name="block_0",
        block=block,
        position=(0.0, 0.0, 0.1),
        orientation=(0.0, 0.0, 0.0, 1.0),
        linear_velocity=(0.0, 0.0, 0.0),
        angular_velocity=(0.0, 0.0, 0.0),
        aabb_min=(-0.1, -0.1, 0.0),
        aabb_max=(0.1, 0.1, 0.2),
    )
    sample = SceneSample(objects=[obj], contacts=[], stable=True, seed=123)
    graph = scene_graph(sample)
    assert graph["objects"][0]["name"] == "block_0"
    assert graph["contacts"] == []
