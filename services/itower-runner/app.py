from fastapi import FastAPI
from pydantic import BaseModel
import requests, os

app = FastAPI(title="itower-runner")

class RunResponse(BaseModel):
    ok: bool

SCENE_URL = os.getenv("SCENE_SERVICE_URL", "http://scene-service")
VERTEX_URL = os.getenv("VERTEX_PROXY_URL", "http://vertex-proxy")
Z3_URL = os.getenv("Z3_CHECKER_URL", "http://z3-checker")

@app.post("/run", response_model=RunResponse)
def run():
    sg = requests.post(f"{SCENE_URL}/analyze", json={"images": []}, timeout=10).json()
    program = requests.post(f"{VERTEX_URL}/infer", json={"prompt":"Is this possible?","images":[]}, timeout=10).json()
    _ = requests.post(f"{Z3_URL}/check", json={"program": program and __import__("json").loads(program.get("content","{}"))}, timeout=10).json()
    return RunResponse(ok=True)
