from pathlib import Path

from support_agent.rag.chunking import chunk_markdown_document
from support_agent.rag.embeddings import EmbeddingService
from support_agent.rag.loaders import load_knowledge_base
from support_agent.rag.search import InMemorySemanticSearch

KNOWLEDGE_BASE_PATH = Path("knowledge_base")


def main() -> None:
    documents = load_knowledge_base(KNOWLEDGE_BASE_PATH)

    chunks = [
        chunk for document in documents for chunk in chunk_markdown_document(document)
    ]

    embedding_service = EmbeddingService()

    search_engine = InMemorySemanticSearch(
        chunks=chunks,
        embedding_service=embedding_service,
    )

    query = input("Enter a question: ")

    results = search_engine.search(
        query=query,
        limit=3,
    )

    print(f"\nQuery: {query}\n")

    for position, result in enumerate(results, start=1):
        print(f"{position}. {result.chunk.document_title}")
        print(f"   Section: {result.chunk.section_title}")
        print(f"   Language: {result.chunk.language.value}")
        print(f"   Score: {result.score:.4f}")
        print(f"   Text: {result.chunk.content}\n")


if __name__ == "__main__":
    main()
