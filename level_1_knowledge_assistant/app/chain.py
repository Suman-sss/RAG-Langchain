"""Chain module placeholder for guided implementation."""
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from app.config import GEN_MODEL, OLLAMA_BASE_URL
from app.prompt_builder import build_prompt


def build_rag_chain():
    prompt = build_prompt()

    llm = ChatOllama(
        model=GEN_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    return chain
