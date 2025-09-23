"""FastAPI service wrapping the Z3 validator."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .z3_rules import validate_program


logger = logging.getLogger("impossible_tower.checker")
logging.basicConfig(level=logging.INFO)


class CheckRequest(BaseModel):
    program: Dict[str, Any]
    scene_graph: Dict[str, Any]
    constraints: Optional[Dict[str, Any]] = None


class CheckResponse(BaseModel):
    pass_: bool = Field(alias="pass")
    violations: list[Dict[str, Any]]
    counterexample: Dict[str, Any]

    class Config:
        allow_population_by_field_name = True


app = FastAPI(title="Impossible Tower Checker", version="0.1.0")


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/check", response_model=CheckResponse)
def check(request: CheckRequest) -> Dict[str, Any]:
    logger.info("Checking program", extra={"assumptions": len(request.program.get("assumptions", []))})
    try:
        result = validate_program(request.program, request.scene_graph, request.constraints)
        return result
    except Exception as exc:  # noqa: BLE001
        logger.exception("Checker failure", exc_info=exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
