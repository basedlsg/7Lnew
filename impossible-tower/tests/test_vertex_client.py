from model.vertex_client import VertexConfig, VertexModelClient


def test_mock_program_without_endpoint(monkeypatch):
    monkeypatch.delenv("VERTEX_ENDPOINT_URL", raising=False)
    client = VertexModelClient(config=VertexConfig(endpoint_url=""))
    program = client.generate_program(["gs://example/cam.png"], "Is this possible?")
    assert "assumptions" in program
    assert "claims" in program
