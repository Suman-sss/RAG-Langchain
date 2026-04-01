"""Embeddings module placeholder for guided implementation."""
from langchain_ollama import OllamaEmbeddings

from app.config import EMBED_MODEL, OLLAMA_BASE_URL


def get_embedding_model():
    embedding_model = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    return embedding_model
