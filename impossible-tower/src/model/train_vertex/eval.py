"""Evaluation harness for Impossible Tower."""

from __future__ import annotations

import json
import pathlib
import statistics
import time
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

import typer


app = typer.Typer(add_completion=False)


@dataclass
class SampleMetrics:
    sample_id: str
    possible_gt: bool
    possible_pred: bool
    violations: int
    counterexample_available: bool
    program_pass: bool


def _load_predictions(path: Optional[str]) -> Dict[str, Dict[str, object]]:
    if not path:
        return {}
    data: Dict[str, Dict[str, object]] = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            data[record["sample_id"]] = record
    return data


def _compute_sample_metrics(sample_dir: pathlib.Path, prediction: Optional[Dict[str, object]]) -> SampleMetrics:
    constraints = json.loads((sample_dir / "constraints.json").read_text())
    label = json.loads((sample_dir / "label.json").read_text())
    sample_id = sample_dir.name
    possible_pred = bool(prediction.get("possible", True)) if prediction else True
    com_constraints = constraints.get("com_constraints", {})
    violations = sum(1 for info in com_constraints.values() if not info.get("within_support", False))
    counterexample_available = violations > 0
    program_pass = violations == 0
    return SampleMetrics(
        sample_id=sample_id,
        possible_gt=bool(label["possible"]),
        possible_pred=possible_pred,
        violations=violations,
        counterexample_available=counterexample_available,
        program_pass=program_pass,
    )


def _summarize(metrics: Iterable[SampleMetrics]) -> Dict[str, float]:
    items = list(metrics)
    if not items:
        raise ValueError("No samples found for evaluation")
    total = len(items)
    acc = sum(m.possible_gt == m.possible_pred for m in items) / total
    program_pass = sum(m.program_pass for m in items) / total
    violation_rate = statistics.mean(m.violations for m in items)
    counterexample_rate = sum(m.counterexample_available for m in items) / total
    cross_view_consistency = 1.0  # Placeholder until multi-view permutations are evaluated
    return {
        "accuracy@1": acc,
        "program_pass_rate": program_pass,
        "violation_rate": violation_rate,
        "counterexample_rate": counterexample_rate,
        "cross_view_consistency": cross_view_consistency,
    }


def _write_markdown(results: Dict[str, float], output_dir: pathlib.Path) -> pathlib.Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path = output_dir / f"eval-{timestamp}.md"
    lines = ["| Metric | Value |", "| ------ | ----- |"]
    for key, value in results.items():
        lines.append(f"| {key} | {value:.3f} |")
    path.write_text("\n".join(lines))
    return path


@app.command()
def main(
    dataset_dir: str = typer.Option(..., help="Path to dataset directory"),
    predictions_path: Optional[str] = typer.Option(None, help="JSONL predictions file"),
    output_dir: str = typer.Option("docs/eval_results", help="Where to store eval tables"),
) -> None:
    dataset_path = pathlib.Path(dataset_dir)
    predictions = _load_predictions(predictions_path)
    metrics = []
    for sample_dir in sorted(dataset_path.iterdir()):
        if sample_dir.is_dir():
            metrics.append(_compute_sample_metrics(sample_dir, predictions.get(sample_dir.name)))
    summary = _summarize(metrics)
    path = _write_markdown(summary, pathlib.Path(output_dir))
    typer.echo(f"Wrote evaluation summary to {path}")


if __name__ == "__main__":
    app()
