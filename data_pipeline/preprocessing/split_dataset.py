from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def split(
    source_path: Path = Path("datasets/processed/training_agri.csv"),
    out_dir: Path = Path("datasets/processed"),
) -> tuple[Path, Path, Path]:
    frame = pd.read_csv(source_path)
    train, temp = train_test_split(frame, test_size=0.3, random_state=42)
    valid, test = train_test_split(temp, test_size=0.5, random_state=42)

    out_dir.mkdir(parents=True, exist_ok=True)
    train_path = out_dir / "train.csv"
    valid_path = out_dir / "valid.csv"
    test_path = out_dir / "test.csv"

    train.to_csv(train_path, index=False)
    valid.to_csv(valid_path, index=False)
    test.to_csv(test_path, index=False)

    return train_path, valid_path, test_path


if __name__ == "__main__":
    paths = split()
    print(f"Dataset split completed: {paths}")
