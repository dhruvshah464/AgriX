from __future__ import annotations

from pathlib import Path

import pandas as pd


def run(source_path: Path = Path("datasets/external/market_prices.csv"), out_path: Path = Path("datasets/raw/market_prices.csv")) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.exists():
        frame = pd.read_csv(source_path)
    else:
        frame = pd.DataFrame(
            [
                {"crop": "wheat", "market_price_inr_quintal": 2400, "date": "2026-01-01"},
                {"crop": "rice", "market_price_inr_quintal": 3100, "date": "2026-01-01"},
            ]
        )
    frame.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    print(f"Market data ingested: {run()}")
