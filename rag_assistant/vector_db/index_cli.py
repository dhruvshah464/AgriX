from __future__ import annotations

import argparse
from pathlib import Path

from rag_assistant.vector_db.index_manager import build_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Build AgriX FAISS vector index from agricultural datasets.")
    parser.add_argument("--index-dir", type=Path, default=Path("rag_assistant/vector_db/faiss_index"))
    parser.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Dataset path to embed. Can be provided multiple times.",
    )
    args = parser.parse_args()

    output = build_index(index_dir=args.index_dir, dataset_paths=args.dataset)
    print(f"Vector index ready at: {output}")


if __name__ == "__main__":
    main()
