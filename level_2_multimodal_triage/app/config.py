from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
GEN_MODEL = os.getenv("GEN_MODEL", "llama3")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

TICKETS_DIR = Path(os.getenv("TICKETS_DIR", "./data/tickets"))
SUPPORT_DOCS_DIR = Path(os.getenv("SUPPORT_DOCS_DIR", "./data/support_docs"))
IMAGES_DIR = Path(os.getenv("IMAGES_DIR", "./data/images"))
EXPECTED_OUTPUTS_DIR = Path(os.getenv("EXPECTED_OUTPUTS_DIR", "./data/expected_outputs"))
VECTOR_STORE_DIR = Path(os.getenv("VECTOR_STORE_DIR", "./storage/chroma"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
TOP_K = int(os.getenv("TOP_K", "4"))

OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "tesseract")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "level_2_multimodal_triage")
