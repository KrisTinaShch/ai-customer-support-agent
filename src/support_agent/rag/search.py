from collections.abc import Sequence
from dataclasses import dataclass

from support_agent.rag.embeddings import EmbeddingService
from support_agent.rag.schemas import KnowledgeChunk


@dataclass(frozen=True)
class SearchResult:
    chunk: KnowledgeChunk
    score: float


class InMemorySemanticSearch:
    def __init__(
        self, chunks: Sequence[KnowledgeChunk], embedding_service: EmbeddingService
    ) -> None:
        self.embedding_service = embedding_service
        self.chunks = list(chunks)
        self.chunk_embeddings = self.embedding_service.embed_chunks(self.chunks)

    def search(self, query: str, limit: int = 3) -> list[SearchResult]:
        if limit < 1:
            raise ValueError("Search limit must be at least 1.")
        if not self.chunks:
            return []

        query_embedding = self.embedding_service.embed_query(query)

        results = [
            SearchResult(
                chunk=chunk,
                score=self._calculate_similarity(
                    query_embedding,
                    chunk_embedding,
                ),
            )
            for chunk, chunk_embedding in zip(
                self.chunks,
                self.chunk_embeddings,
                strict=True,
            )
        ]
        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:limit]

    @staticmethod
    def _calculate_similarity(
        left: Sequence[float],
        right: Sequence[float],
    ) -> float:
        return sum(
            left_value * right_value
            for left_value, right_value in zip(left, right, strict=True)
        )
