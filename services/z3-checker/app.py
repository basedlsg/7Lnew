from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="z3-checker")

class CheckRequest(BaseModel):
    program: dict
    scene_graph_uri: str | None = None

class CheckResponse(BaseModel):
    result: str
    rationale: str | None = None

@app.post("/check", response_model=CheckResponse)
def check(req: CheckRequest):
    claims = req.program.get("claims", [])
    if any("unstable(scene)" in c for c in claims):
        return CheckResponse(result="unsat", rationale="Claimed unstable")
    return CheckResponse(result="sat", rationale="Heuristic pass")
