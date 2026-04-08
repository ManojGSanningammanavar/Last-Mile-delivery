from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.run_training_pipeline import run_training


if __name__ == "__main__":
    metrics = run_training()
    print("Training completed")
    print(metrics)
