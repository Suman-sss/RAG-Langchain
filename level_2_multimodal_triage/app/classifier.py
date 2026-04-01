from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.config import GEN_MODEL, OLLAMA_BASE_URL


def build_classifier():
    prompt = ChatPromptTemplate.from_template(
        """
You are a support triage classifier.

Classify the support issue into exactly one of these categories:
- vpn_access
- mfa_issue
- account_recovery
- device_provisioning
- repository_access
- unknown

Return only the category name.
Do not explain your answer.

Issue Text:
{issue_text}
"""
    )

    llm = ChatOllama(
        model=GEN_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )

    parser = StrOutputParser()

    classifier_chain = prompt | llm | parser

    return classifier_chain
