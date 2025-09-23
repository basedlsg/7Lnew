from fastapi.testclient import TestClient

from checker.service import app


client = TestClient(app)


def test_checker_passes_valid_program():
    payload = {
        "program": {
            "assumptions": [
                "contact(block_1,block_0)",
                "support(block_1,block_0)",
                "com_within_support(block_1)",
            ],
            "claims": ["stable(scene)"],
        },
        "scene_graph": {
            "objects": [
                {
                    "name": "block_0",
                    "support_polygon_xy": [[-0.2, -0.2], [0.2, -0.2], [0.2, 0.2], [-0.2, 0.2]],
                },
                {
                    "name": "block_1",
                    "support_polygon_xy": [[-0.1, -0.1], [0.1, -0.1], [0.1, 0.1], [-0.1, 0.1]],
                },
            ],
            "contacts": [
                {"body_a": "block_1", "body_b": "block_0", "normal": (0.0, 0.0, 1.0)}
            ],
        },
        "constraints": {
            "com_constraints": {
                "block_1": {
                    "com_xy": [0.0, 0.0],
                    "supporters": ["block_0"],
                    "support_polygons": [[[-0.2, -0.2], [0.2, -0.2], [0.2, 0.2], [-0.2, 0.2]]],
                    "within_support": True,
                }
            }
        },
    }
    response = client.post("/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pass"] is True


def test_checker_flags_missing_contact():
    payload = {
        "program": {"assumptions": ["contact(block_1,block_0)"], "claims": []},
        "scene_graph": {"contacts": []},
        "constraints": {},
    }
    response = client.post("/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pass"] is False
    assert data["violations"]
