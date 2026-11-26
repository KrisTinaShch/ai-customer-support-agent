from support_agent.rag.schemas import KnowledgeChunk, KnowledgeDocument

TOP_LEVEL_HEADING_PREFIX = "# "
SECTION_HEADING_PREFIX = "## "


def _build_chunk(
    document: KnowledgeDocument,
    section_title: str | None,
    content: str,
    chunk_index: int,
) -> KnowledgeChunk:
    return KnowledgeChunk(
        chunk_id=f"{document.document_id}:{chunk_index}",
        document_id=document.document_id,
        source_id=document.source_id,
        language=document.language,
        category=document.category,
        document_title=document.title,
        section_title=section_title,
        chunk_index=chunk_index,
        version=document.version,
        updated_at=document.updated_at,
        content=content,
        source_path=document.source_path,
    )


def chunk_markdown_document(
    document: KnowledgeDocument,
) -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []

    section_title: str | None = None
    section_lines: list[str] = []

    for line in document.content.splitlines():
        if line.startswith(SECTION_HEADING_PREFIX):
            section_content = "\n".join(section_lines).strip()

            if section_content:
                chunks.append(
                    _build_chunk(
                        document=document,
                        section_title=section_title,
                        content=section_content,
                        chunk_index=len(chunks),
                    )
                )

            section_title = line.removeprefix(SECTION_HEADING_PREFIX).strip()
            section_lines = []
            continue

        if line.startswith(TOP_LEVEL_HEADING_PREFIX):
            continue

        section_lines.append(line)

    final_content = "\n".join(section_lines).strip()

    if final_content:
        chunks.append(
            _build_chunk(
                document=document,
                section_title=section_title,
                content=final_content,
                chunk_index=len(chunks),
            )
        )

    return chunks
