from __future__ import annotations

import argparse
import os
from pathlib import Path

from rag_assistant.chatbot.assistant import ask_assistant
from rag_assistant.vector_db.index_manager import build_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Query AgriX LangChain+FAISS farming assistant.")
    parser.add_argument("--query", required=True, help="Farming question to ask.")
    parser.add_argument("--provider", default="openai", help="LLM provider name.")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model name.")
    parser.add_argument("--api-key", default=None, help="Provider API key. Defaults to OPENAI_API_KEY env var.")
    parser.add_argument("--index-dir", type=Path, default=Path("rag_assistant/vector_db/faiss_index"))
    parser.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Dataset path to embed before querying. Can be provided multiple times.",
    )
    args = parser.parse_args()

    build_index(index_dir=args.index_dir, dataset_paths=args.dataset)

    answer, sources = ask_assistant(
        query=args.query,
        provider=args.provider,
        model_name=args.model,
        api_key=args.api_key or os.getenv("OPENAI_API_KEY"),
        index_dir=args.index_dir,
    )
    print({"answer": answer, "sources": sources})


if __name__ == "__main__":
    main()
