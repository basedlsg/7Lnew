"""Client for calling a Vertex AI multimodal endpoint."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, MutableMapping, Sequence

import google.auth
from google.auth.transport.requests import Request
import requests

from .formatter import FewShotExample, build_prompt, json_schema_template


TRUE_VALUES = {"1", "true", "yes", "on"}


@dataclass
class VertexConfig:
    endpoint_url: str = field(default_factory=lambda: os.getenv("VERTEX_ENDPOINT_URL", ""))
    endpoint_id: str = field(default_factory=lambda: os.getenv("VERTEX_ENDPOINT_ID", ""))
    project_id: str = field(default_factory=lambda: os.getenv("VERTEX_PROJECT_ID", ""))
    location: str = field(default_factory=lambda: os.getenv("VERTEX_LOCATION", ""))
    api_key: str = field(default_factory=lambda: os.getenv("VERTEX_API_KEY", ""))
    publisher_model: str = field(default_factory=lambda: os.getenv("VERTEX_PUBLISHER_MODEL", ""))
    use_publisher_model: bool = field(default_factory=lambda: os.getenv("USE_VERTEX_PUBLISHER_MODEL", "").lower() in TRUE_VALUES)
    temperature: float = field(default_factory=lambda: float(os.getenv("VERTEX_TEMPERATURE", "0.0")))
    max_output_tokens: int = field(default_factory=lambda: int(os.getenv("VERTEX_MAX_OUTPUT_TOKENS", "1024")))


class VertexModelClient:
    def __init__(self, config: VertexConfig | None = None, session: requests.Session | None = None) -> None:
        self.config = config or VertexConfig()
        self.session = session or requests.Session()
        self._examples: list[FewShotExample] = []

    def register_example(self, example: FewShotExample) -> None:
        self._examples.append(example)

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _mock_program(self, images: Sequence[str]) -> Mapping[str, object]:
        return {
            "assumptions": ["contact(block_1,block_0)", "support(block_1,block_0)", "com_within_support(block_1)"],
            "claims": ["stable(scene)"]
            if "impossible" not in "".join(images)
            else ["unstable(scene)"],
            "view_refs": list(images[:2]),
        }

    def generate_program(self, images: Sequence[str], question: str) -> Mapping[str, object]:
        if self.config.use_publisher_model and self.config.publisher_model:
            return self._predict_publisher_model(images, question)

        if not self.config.endpoint_url:
            return self._mock_program(images)

        payload = {
            "instances": [
                {
                    "prompt": build_prompt(question, images, self._examples),
                    "images": images,
                    "response_schema": json_schema_template(),
                }
            ]
        }
        response = self.session.post(
            self.config.endpoint_url,
            headers=self._headers(),
            data=json.dumps(payload),
            timeout=90,
        )
        response.raise_for_status()
        body = response.json()
        try:
            predictions = body["predictions"]
            if not predictions:
                raise ValueError("Empty response from Vertex")
            raw_text = predictions[0].get("content", "{}").strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("`\n")
            return json.loads(raw_text)
        except (KeyError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Failed to parse Vertex response: {body}") from exc

    def _predict_publisher_model(self, images: Sequence[str], question: str) -> Mapping[str, object]:
        if not self.config.project_id or not self.config.location:
            raise RuntimeError("VERTEX_PROJECT_ID and VERTEX_LOCATION must be set for publisher models")

        prompt = build_prompt(question, images, self._examples)
        instances = [
            {
                "prompt": {"text": prompt},
                "images": [{"gcsUri": uri} for uri in images],
            }
        ]
        payload = {
            "instances": instances,
            "parameters": {
                "temperature": self.config.temperature,
                "maxOutputTokens": self.config.max_output_tokens,
            },
            "prediction_params": {"response_mime_type": "application/json"},
        }

        credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        credentials.refresh(Request())
        url = (
            f"https://{self.config.location}-aiplatform.googleapis.com/v1/projects/"
            f"{self.config.project_id}/locations/{self.config.location}/publishers/google/models/"
            f"{self.config.publisher_model}:predict"
        )
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        }
        response = self.session.post(url, headers=headers, data=json.dumps(payload), timeout=120)
        response.raise_for_status()
        body = response.json()
        try:
            predictions = body.get("predictions", [])
            if not predictions:
                raise ValueError("Empty response from publisher model")
            prediction = predictions[0]
            raw_text = None
            if isinstance(prediction, dict):
                if isinstance(prediction.get("content"), str):
                    raw_text = prediction["content"]
                elif "candidates" in prediction:
                    candidates = prediction.get("candidates", [])
                    if candidates:
                        candidate = candidates[0]
                        parts = candidate.get("content", {}).get("parts", [])
                        raw_text = "".join(part.get("text", "") for part in parts)
                elif isinstance(prediction.get("prediction"), str):
                    raw_text = prediction["prediction"]
            if not raw_text:
                raw_text = json.dumps(prediction)
            raw_text = raw_text.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("`\n")
            return json.loads(raw_text)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Failed to parse publisher model response: {body}") from exc


def default_client() -> VertexModelClient:
    client = VertexModelClient()
    if not client.config.endpoint_url:
        example = FewShotExample(
            question="Is this stack physically possible?",
            images=["gs://bucket/sample/cam_00.png"],
            program={
                "assumptions": ["contact(block_1,block_0)", "support(block_1,block_0)", "com_within_support(block_1)"],
                "claims": ["stable(scene)"]
            },
            rationale="Block 1 rests on block 0 and its COM lies within the support polygon.",
        )
        client.register_example(example)
    return client
