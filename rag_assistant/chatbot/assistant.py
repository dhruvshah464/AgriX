from __future__ import annotations

from pathlib import Path

from rag_assistant.chatbot.prompts import SYSTEM_PROMPT
from rag_assistant.vector_db.retriever import retrieve_documents

try:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
except Exception:  # pragma: no cover
    ChatPromptTemplate = None
    StrOutputParser = None

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

try:
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover
    ChatOpenAI = None


def _build_prompt(query: str, docs: list[str]) -> str:
    context = "\n".join(f"- {doc}" for doc in docs)
    if ChatPromptTemplate is None:
        return f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nUser question: {query}"

    template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Context:\n{context}\n\nQuestion: {query}\nProvide practical farming actions.",
            ),
        ]
    )
    rendered = template.format(context=context, query=query)

    if StrOutputParser is None:
        return str(rendered)
    parser = StrOutputParser()
    return parser.parse(str(rendered))


def ask_assistant(
    query: str,
    provider: str,
    model_name: str,
    api_key: str | None,
    index_dir: str | Path = Path("rag_assistant/vector_db/faiss_index"),
) -> tuple[str, list[str]]:
    docs_with_meta = retrieve_documents(query=query, top_k=4, index_dir=Path(index_dir))
    docs = [item["text"] for item in docs_with_meta]
    if not docs:
        docs = ["No indexed agronomy documents found. Provide general best-practice guidance."]

    prompt = _build_prompt(query, docs)

    if provider.lower() == "openai" and api_key:
        if ChatOpenAI and ChatPromptTemplate and StrOutputParser:
            llm = ChatOpenAI(model=model_name, api_key=api_key, temperature=0.2)
            prompt_template = ChatPromptTemplate.from_messages(
                [
                    ("system", SYSTEM_PROMPT),
                    ("human", "Context:\n{context}\n\nQuestion: {query}"),
                ]
            )
            chain = prompt_template | llm | StrOutputParser()
            answer = chain.invoke({"context": "\n".join(f"- {d}" for d in docs), "query": query})
            return answer, docs

        if OpenAI:
            client = OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            answer = completion.choices[0].message.content or "No response generated."
            return answer, docs

    answer = (
        "Based on retrieved agronomy guidance: optimize nutrient balance, align irrigation with forecasted rainfall, "
        "and investigate low-NDVI areas for stress and pest risk."
    )
    return answer, docs
