import yaml

FRONT_MATTER_DELIMITER = "---"


class InvalidKnowledgeDocumentError(ValueError):
    pass


def parse_markdown_document(
    raw_text: str,
) -> tuple[dict[str, object], str]:
    normalized_text = raw_text.lstrip("\ufeff")

    parts = normalized_text.split(FRONT_MATTER_DELIMITER, maxsplit=2)

    if len(parts) != 3 or parts[0].strip():
        raise InvalidKnowledgeDocumentError(
            "Document must start with YAML front matter"
        )

    metadata_text = parts[1].strip()
    content = parts[2].strip()

    try:
        metadata = yaml.safe_load(metadata_text)
    except yaml.YAMLError as error:
        raise InvalidKnowledgeDocumentError(
            "Document metadata contains invalid YAML."
        ) from error
    if not isinstance(metadata, dict):
        raise InvalidKnowledgeDocumentError("Document metadata must be a YAML mapping.")

    if not content:
        raise InvalidKnowledgeDocumentError("Document content cannot be empty.")

    return metadata, content
