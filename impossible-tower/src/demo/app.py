"""FastAPI demo service orchestrating model inference and proof checking."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from model.vertex_client import default_client


logger = logging.getLogger("impossible_tower.demo")
logging.basicConfig(level=logging.INFO)

CHECKER_URL = os.getenv("CHECKER_SERVICE_URL", "http://localhost:8081/check")

app = FastAPI(title="Impossible Tower Demo", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    images: List[str] = Field(..., description="List of image URIs (GCS paths)")
    question: str = Field("Is this stack physically possible?", description="Natural language question")
    scene_graph: Optional[Dict[str, Any]] = Field(None, description="Scene graph JSON")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Constraint JSON")


class AnalyzeResponse(BaseModel):
    possible: bool
    program: Dict[str, Any]
    proof: Dict[str, Any]
    explanation: str


_vertex_client = default_client()


async def _call_checker(
    program: Dict[str, Any],
    scene_graph: Optional[Dict[str, Any]],
    constraints: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    payload = {"program": program, "scene_graph": scene_graph or {}, "constraints": constraints or {}}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(CHECKER_URL, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:  # noqa: BLE001
        logger.error("Checker call failed: %s", exc)
        raise HTTPException(status_code=502, detail=f"Checker call failed: {exc}") from exc


@app.get("/healthz")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    if not request.images:
        raise HTTPException(status_code=400, detail="No images provided")
    program = _vertex_client.generate_program(request.images, request.question)
    proof = await _call_checker(program, request.scene_graph, request.constraints)
    possible = any("stable(scene)" in claim for claim in program.get("claims", [])) and proof.get("pass", False)
    explanation = "Stable" if possible else "Detected constraint violations"
    return AnalyzeResponse(possible=possible, program=program, proof=proof, explanation=explanation)
