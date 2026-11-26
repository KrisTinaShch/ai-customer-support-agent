from pathlib import Path

import pytest

from support_agent.rag.chunking import chunk_markdown_document
from support_agent.rag.loaders import load_markdown_document
from support_agent.rag.schemas import DocumentLanguage


@pytest.mark.parametrize(
    (
        "file_name",
        "document_id",
        "language",
        "expected_titles",
        "expected_phrase",
    ),
    [
        (
            "returns.en.md",
            "returns-policy-en",
            DocumentLanguage.ENGLISH,
            [
                "Return eligibility",
                "Non-returnable products",
                "Damaged or incorrect products",
                "Return process",
                "Refunds",
            ],
            "Opened memory cards",
        ),
        (
            "returns.bg.md",
            "returns-policy-bg",
            DocumentLanguage.BULGARIAN,
            [
                "Условия за връщане",
                "Продукти, които не подлежат на връщане",
                "Повредени или неправилно доставени продукти",
                "Процес на връщане",
                "Възстановяване на суми",
            ],
            "Отворени карти с памет",
        ),
    ],
)
def test_chunk_markdown_document_by_sections(
    file_name: str,
    document_id: str,
    language: DocumentLanguage,
    expected_titles: list[str],
    expected_phrase: str,
) -> None:
    document_path = Path("knowledge_base/policies") / file_name

    document = load_markdown_document(document_path)
    chunks = chunk_markdown_document(document)

    assert len(chunks) == len(expected_titles)

    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))

    assert [chunk.section_title for chunk in chunks] == expected_titles

    assert [chunk.chunk_id for chunk in chunks] == [
        f"{document_id}:{index}" for index in range(len(chunks))
    ]

    assert all(chunk.document_id == document_id for chunk in chunks)

    assert all(chunk.language is language for chunk in chunks)

    assert expected_phrase in chunks[1].content
