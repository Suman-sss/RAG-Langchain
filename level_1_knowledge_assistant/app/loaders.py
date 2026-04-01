"""Loader module placeholder for guided implementation."""
from pathlib import Path

from langchain_core.documents import Document

from app.config import DOCUMENTS_DIR, IMAGE_DESCRIPTIONS_DIR


def load_text_documents(directory: Path) -> list[Document]:
    documents = []

    for file_path in sorted(directory.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "data_type": "text",
                },
            )
        )

    return documents


def load_image_description_documents(directory: Path) -> list[Document]:
    documents = []

    for file_path in sorted(directory.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name,
                    "data_type": "image_description",
                },
            )
        )

    return documents


def load_all_documents() -> list[Document]:
    text_documents = load_text_documents(DOCUMENTS_DIR)
    image_documents = load_image_description_documents(IMAGE_DESCRIPTIONS_DIR)

    return text_documents + image_documents
