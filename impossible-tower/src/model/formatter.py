"""Prompt and structured output helpers for the Vertex model client."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, List, Mapping, Sequence


@dataclass
class FewShotExample:
    question: str
    images: Sequence[str]
    program: Mapping[str, object]
    rationale: str


def format_example(example: FewShotExample) -> str:
    parts = ["<example>"]
    parts.append(f"question: {example.question}")
    parts.append(f"images: {', '.join(example.images)}")
    parts.append("program:")
    parts.append(json.dumps(example.program, indent=2))
    parts.append(f"rationale: {example.rationale}")
    parts.append("</example>")
    return "\n".join(parts)


def build_prompt(question: str, images: Sequence[str], examples: Iterable[FewShotExample]) -> str:
    exemplar_str = "\n\n".join(format_example(e) for e in examples)
    user_block = ["<task>", "You are a physics reasoning assistant.", "Return a JSON program describing assumptions and claims about the scene.", "</task>"]
    prompt = "\n\n".join(
        [
            exemplar_str,
            "\n".join(user_block),
            f"question: {question}",
            f"images: {', '.join(images)}",
            "Return only JSON with keys: assumptions, claims, view_refs.",
        ]
    ).strip()
    return prompt


def json_schema_template() -> Mapping[str, object]:
    return {
        "type": "object",
        "properties": {
            "assumptions": {
                "type": "array",
                "items": {"type": "string"}
            },
            "claims": {
                "type": "array",
                "items": {"type": "string"}
            },
            "view_refs": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["assumptions", "claims"],
    }
