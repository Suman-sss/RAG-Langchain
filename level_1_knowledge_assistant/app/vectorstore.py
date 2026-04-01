"""Vector store module placeholder for guided implementation."""
from langchain_chroma import Chroma

from app.config import VECTOR_STORE_DIR
from app.embeddings import get_embedding_model


def build_vector_store(split_docs):
    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=str(VECTOR_STORE_DIR),
    )

    return vector_store
