"""Configuration placeholder for guided implementation."""
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
GEN_MODEL = os.getenv("GEN_MODEL", "llama3")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DOCUMENTS_DIR = Path(os.getenv("DOCUMENTS_DIR", "./data/documents"))
IMAGE_DESCRIPTIONS_DIR = Path(os.getenv("IMAGE_DESCRIPTIONS_DIR", "./data/image_descriptions"))
VECTOR_STORE_DIR = Path(os.getenv("VECTOR_STORE_DIR", "./storage/chroma"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
TOP_K = int(os.getenv("TOP_K", "3"))
