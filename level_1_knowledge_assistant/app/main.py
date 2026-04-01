"""Entry point placeholder for guided implementation."""
from app.chain import build_rag_chain
from app.loaders import load_all_documents
from app.retriever import get_retriever
from app.splitter import split_documents
from app.vectorstore import build_vector_store

def deduplicate_documents(documents):
    unique_documents = []
    seen = set()

    for document in documents:
        key = (
            document.metadata.get("source", ""),
            document.page_content.strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_documents.append(document)

    return unique_documents


def format_context(documents):
    context_parts = []

    for document in documents:
        source = document.metadata.get("source", "unknown")
        data_type = document.metadata.get("data_type", "unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"Data Type: {data_type}\n"
            f"Content: {document.page_content}"
        )

    return "\n\n".join(context_parts)


def main():
    documents = load_all_documents()
    split_docs = split_documents(documents)
    vector_store = build_vector_store(split_docs)
    retriever = get_retriever(vector_store)
    rag_chain = build_rag_chain()

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(split_docs)} chunks.\n")

    question = input("Ask a question: ").strip()

    retrieved_docs = retriever.invoke(question)
    retrieved_docs = deduplicate_documents(retrieved_docs)


    if not retrieved_docs:
        print("I do not know based on the provided knowledge sources.")
        return

    context = format_context(retrieved_docs)

    answer = rag_chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    print("\nRetrieved Context:\n")
    for document in retrieved_docs:
        print(document.metadata.get("source", "unknown"))
        print(document.page_content)
        print()

    print("Generated Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()
