"""Retriever module placeholder for guided implementation."""
from app.config import TOP_K


def get_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": TOP_K}
    )

    return retriever
