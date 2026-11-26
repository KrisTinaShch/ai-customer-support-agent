from datetime import date
from pathlib import Path

import pytest

from support_agent.rag.loaders import (
    InvalidKnowledgeDocumentError,
    load_markdown_document,
    parse_markdown_document,
)
from support_agent.rag.schemas import DocumentCategory, DocumentLanguage


def test_load_markdown_document(tmp_path: Path) -> None:
    document_path = tmp_path / "returns.en.md"

    document_path.write_text(
        """---
document_id: returns-policy-en
source_id: returns-policy
language: en
category: policy
title: Returns and refunds
version: 1.0
updated_at: 2026-11-25
---

# Returns and refunds

Unused products can be returned within 14 calendar days.
""",
        encoding="utf-8",
    )

    document = load_markdown_document(document_path)

    assert document.document_id == "returns-policy-en"
    assert document.source_id == "returns-policy"
    assert document.language is DocumentLanguage.ENGLISH
    assert document.category is DocumentCategory.POLICY
    assert document.title == "Returns and refunds"
    assert document.version == "1.0"
    assert document.updated_at == date(2026, 11, 25)
    assert "14 calendar days" in document.content
    assert document.source_path == document_path


@pytest.mark.parametrize(
    ("raw_text", "expected_message"),
    [
        (
            "# Document without metadata",
            "Document must start with YAML front matter",
        ),
        (
            "---\n- list item\n---\n# Content",
            "Document metadata must be a YAML mapping",
        ),
        (
            "---\nlanguage: [\n---\n# Content",
            "Document metadata contains invalid YAML",
        ),
        (
            "---\nlanguage: en\n---\n",
            "Document content cannot be empty",
        ),
    ],
)
def test_parse_markdown_document_rejects_invalid_input(
    raw_text: str,
    expected_message: str,
) -> None:
    with pytest.raises(
        InvalidKnowledgeDocumentError,
        match=expected_message,
    ):
        parse_markdown_document(raw_text)
