from collections.abc import Sequence

from sentence_transformers import SentenceTransformer

from support_agent.rag.schemas import KnowledgeChunk

DEFAULT_MODEL_NAME = "intfloat/multilingual-e5-small"


class EmbeddingService:
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        query_prefix: str = "query: ",
        passage_prefix: str = "passage: ",
    ) -> None:
        self.model = SentenceTransformer(model_name)
        self.query_prefix = query_prefix
        self.passage_prefix = passage_prefix

    def embed_query(self, query: str) -> list[float]:
        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("Query must not be empty.")

        embedding = self.model.encode(
            self.query_prefix + cleaned_query,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embedding.tolist()

    def embed_chunks(self, chunks: Sequence[KnowledgeChunk]) -> list[list[float]]:
        if not chunks:
            return []

        passages = [self._prepare_passage(chunk) for chunk in chunks]

        embeddings = self.model.encode(
            passages,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def _prepare_passage(self, chunk: KnowledgeChunk) -> str:
        parts = [chunk.document_title]

        if chunk.section_title:
            parts.append(chunk.section_title)

        parts.append(chunk.content)

        passage = "\n\n".join(parts)

        return self.passage_prefix + passage
