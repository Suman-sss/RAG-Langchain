from pathlib import Path

from langchain_core.documents import Document

from app.config import SUPPORT_DOCS_DIR, TICKETS_DIR


def load_support_documents(directory: Path) -> list[Document]:
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
                    "source_type": "support_doc",
                },
            )
        )

    return documents


def load_ticket_documents(directory: Path) -> list[Document]:
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
                    "source_type": "ticket",
                },
            )
        )

    return documents


def load_all_text_documents() -> list[Document]:
    support_documents = load_support_documents(SUPPORT_DOCS_DIR)
    ticket_documents = load_ticket_documents(TICKETS_DIR)

    return support_documents + ticket_documents
