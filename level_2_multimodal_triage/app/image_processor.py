from pathlib import Path

import pytesseract
from PIL import Image
from langchain_core.documents import Document

from app.config import IMAGES_DIR, OCR_LANGUAGE, TESSERACT_CMD


pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def extract_text_from_image(image_path: Path) -> str:
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image, lang=OCR_LANGUAGE)

    return extracted_text.strip()


def load_image_documents(directory: Path) -> list[Document]:
    documents = []

    for file_path in sorted(directory.glob("*")):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".bmp"}:
            continue

        extracted_text = extract_text_from_image(file_path)

        if not extracted_text:
            continue

        documents.append(
            Document(
                page_content=extracted_text,
                metadata={
                    "source": file_path.name,
                    "source_type": "image_ocr",
                },
            )
        )

    return documents


def load_all_image_documents() -> list[Document]:
    return load_image_documents(IMAGES_DIR)
