from pathlib import Path

from app.chain import build_triage_chain
from app.classifier import build_classifier
from app.evaluator import compare_outputs, load_expected_output
from app.image_processor import load_all_image_documents
from app.loaders import load_all_text_documents
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
        source_type = document.metadata.get("source_type", "unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"Source Type: {source_type}\n"
            f"Content: {document.page_content}"
        )

    return "\n\n".join(context_parts)


def build_expected_output_file_name(ticket_file_name: str) -> str:
    ticket_path = Path(ticket_file_name)
    return f"{ticket_path.stem}_expected.txt"


def main():
    text_documents = load_all_text_documents()
    image_documents = load_all_image_documents()
    all_documents = text_documents + image_documents

    split_docs = split_documents(all_documents)
    vector_store = build_vector_store(split_docs)
    retriever = get_retriever(vector_store)

    classifier = build_classifier()
    triage_chain = build_triage_chain()

    print(f"Loaded {len(text_documents)} text documents.")
    print(f"Loaded {len(image_documents)} OCR image documents.")
    print(f"Created {len(split_docs)} chunks.\n")

    ticket_file_name = input("Enter ticket file name: ").strip()

    matching_ticket = None
    for document in text_documents:
        if (
            document.metadata.get("source") == ticket_file_name
            and document.metadata.get("source_type") == "ticket"
        ):
            matching_ticket = document
            break

    if matching_ticket is None:
        print("Ticket not found.")
        return

    issue_text = matching_ticket.page_content
    predicted_category = classifier.invoke({"issue_text": issue_text}).strip()

    retrieved_docs = retriever.invoke(issue_text)
    retrieved_docs = deduplicate_documents(retrieved_docs)

    if not retrieved_docs:
        print("No relevant support context found.")
        return

    context = format_context(retrieved_docs)

    triage_response = triage_chain.invoke(
        {
            "context": context,
            "issue_text": issue_text,
            "issue_category": predicted_category,
        }
    )

    expected_file_name = build_expected_output_file_name(ticket_file_name)
    expected_output = load_expected_output(expected_file_name)
    evaluation_result = compare_outputs(triage_response, expected_output)

    print(f"\nPredicted Category: {predicted_category}\n")

    print("Retrieved Context:\n")
    for document in retrieved_docs:
        print(document.metadata.get("source", "unknown"))
        print(document.metadata.get("source_type", "unknown"))
        print(document.page_content)
        print()

    print("Generated Triage Response:\n")
    print(triage_response)

    print("\nEvaluation Summary:\n")
    print(f"Expected Output Available: {evaluation_result['expected_available']}")
    print(f"Exact Match: {evaluation_result['exact_match']}")

    if evaluation_result["expected_available"]:
        print("\nExpected Output:\n")
        print(evaluation_result["expected_output"])


if __name__ == "__main__":
    main()
