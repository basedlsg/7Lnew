"""Vertex CustomJob entrypoint for LoRA fine-tuning."""

from __future__ import annotations

import json
import pathlib
from dataclasses import asdict, dataclass

import typer


app = typer.Typer(add_completion=False)


@dataclass
class TrainConfig:
    train_data: str
    eval_data: str
    output_dir: str
    model_name: str = "paligemma"
    lora_rank: int = 16
    epochs: int = 3
    learning_rate: float = 2e-4
    batch_size: int = 4


@app.command()
def main(
    train_data: str = typer.Option(..., help="GCS URI to training data"),
    eval_data: str = typer.Option(..., help="GCS URI to evaluation data"),
    output_dir: str = typer.Option(..., help="GCS URI where artifacts should be written"),
    model_name: str = typer.Option("paligemma", help="Base model name"),
    lora_rank: int = typer.Option(16, help="Low-rank adaptation rank"),
    epochs: int = typer.Option(3, help="Number of fine-tuning epochs"),
    learning_rate: float = typer.Option(2e-4, help="Learning rate"),
    batch_size: int = typer.Option(4, help="Batch size per device"),
) -> None:
    config = TrainConfig(
        train_data=train_data,
        eval_data=eval_data,
        output_dir=output_dir,
        model_name=model_name,
        lora_rank=lora_rank,
        epochs=epochs,
        learning_rate=learning_rate,
        batch_size=batch_size,
    )
    typer.echo(f"[trainer] Starting job with config: {config}")
    # Placeholder implementation: in the initial scaffold we emit the config to a metadata file.
    metadata = {
        "status": "NOT_IMPLEMENTED",
        "message": "Implement LoRA fine-tuning pipeline.",
        "config": asdict(config),
    }
    output_path = pathlib.Path("trainer_config.json")
    output_path.write_text(json.dumps(metadata, indent=2))
    typer.echo("[trainer] Wrote trainer_config.json with metadata stub.")


if __name__ == "__main__":
    app()
