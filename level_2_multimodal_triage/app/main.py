from pathlib import Path

from app.chain import build_triage_chain
from app.classifier import build_classifier
from app.evaluator import compare_outputs, load_expected_output
from app.image_processor import load_all_image_documents
from app.loaders import load_all_text_documents
from app.retriever import retrieve_documents
from app.splitter import split_documents
from app.vectorstore import build_vector_store
import re


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

def extract_attached_image_name(ticket_text: str) -> str | None:
    match = re.search(r"Attached Image:\s*(.+)", ticket_text)

    if not match:
        return None

    image_name = match.group(1).strip()

    if image_name.lower() == "none":
        return None

    return image_name


def find_image_document_by_source(image_name: str, image_documents):
    for document in image_documents:
        if document.metadata.get("source") == image_name:
            return document

    return None

def build_sources_line(documents, attached_image_name=None):
    source_names = []
    seen = set()

    for document in documents:
        source_name = document.metadata.get("source", "").strip()
        source_type = document.metadata.get("source_type", "").strip()

        if not source_name:
            continue

        if source_type == "support_doc" and source_name not in seen:
            seen.add(source_name)
            source_names.append(source_name)

    if attached_image_name and attached_image_name not in seen:
        seen.add(attached_image_name)
        source_names.append(attached_image_name)

    if not source_names:
        for document in documents:
            source_name = document.metadata.get("source", "").strip()

            if not source_name:
                continue

            if source_name in seen:
                continue

            seen.add(source_name)
            source_names.append(source_name)

    if not source_names:
        return "Sources: None"

    return f"Sources: {', '.join(source_names)}"


def normalize_triage_response(triage_response: str, documents, attached_image_name=None):
    lines = [line.strip() for line in triage_response.splitlines() if line.strip()]

    filtered_lines = []
    for line in lines:
        if line.startswith("Sources:"):
            continue
        filtered_lines.append(line)

    sources_line = build_sources_line(documents, attached_image_name=attached_image_name)

    if len(filtered_lines) >= 3:
        normalized_lines = filtered_lines[:3] + [sources_line]
    else:
        normalized_lines = filtered_lines + [sources_line]

    return "\n".join(normalized_lines)


def main():
    text_documents = load_all_text_documents()
    image_documents = load_all_image_documents()
    all_documents = text_documents + image_documents

    split_docs = split_documents(all_documents)
    vector_store = build_vector_store(split_docs)

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
    attached_image_name = extract_attached_image_name(issue_text)
    attached_image_document = None

    if attached_image_name:
        attached_image_document = find_image_document_by_source(
            attached_image_name,
            image_documents,
        )

    predicted_category = classifier.invoke({"issue_text": issue_text}).strip()

    retrieved_docs = retrieve_documents(
        issue_text,
        vector_store,
        attached_image_document=attached_image_document,
    )

    retrieved_docs = deduplicate_documents(retrieved_docs)

    if attached_image_document is not None:
        retrieved_docs = [attached_image_document] + retrieved_docs
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

    triage_response = normalize_triage_response(
        triage_response,
        retrieved_docs,
        attached_image_name=attached_image_name,
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
    print(f"Normalized Match: {evaluation_result.get('normalized_match', False)}")

    if evaluation_result["expected_available"]:
        print("\nExact Field Matches:\n")
        for field_name, field_match in evaluation_result["exact_field_matches"].items():
            print(f"{field_name}: {field_match}")

        print("\nNormalized Field Matches:\n")
        for field_name, field_match in evaluation_result["normalized_field_matches"].items():
            print(f"{field_name}: {field_match}")

        print("\nSource Overlap:\n")
        for metric_name, metric_value in evaluation_result["source_overlap"].items():
            print(f"{metric_name}: {metric_value}")

        print("\nGenerated Fields:\n")
        for field_name, field_value in evaluation_result["generated_fields"].items():
            print(f"{field_name}: {field_value}")

        print("\nExpected Fields:\n")
        for field_name, field_value in evaluation_result["expected_fields"].items():
            print(f"{field_name}: {field_value}")

        print("\nExpected Output:\n")
        print(evaluation_result["expected_output"])




if __name__ == "__main__":
    main()
