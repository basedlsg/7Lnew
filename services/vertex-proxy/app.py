from fastapi import FastAPI
from pydantic import BaseModel
import os, json

app = FastAPI(title="vertex-proxy")

class InferRequest(BaseModel):
    prompt: str
    images: list[str] = []
    response_schema: dict | None = None

class InferResponse(BaseModel):
    content: str

@app.post("/infer", response_model=InferResponse)
def infer(req: InferRequest):
    # Deterministic mock content that matches contracts/examples/possible.json
    program = {
        "assumptions": [
            "contact(block_1,block_0)",
            "support(block_1,block_0)",
            "com_within_support(block_1)"
        ],
        "claims": ["stable(scene)"],
        "view_refs": req.images[:2]
    }
    return InferResponse(content=json.dumps(program))
