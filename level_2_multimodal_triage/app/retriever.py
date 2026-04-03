from app.config import TOP_K


SOURCE_LIMITS = {
    "support_doc": 2,
    "image_ocr": 1,
    "ticket": 1,
}


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


def retrieve_by_source_type(query: str, vector_store, source_type: str, limit: int):
    documents = vector_store.similarity_search(
        query,
        k=max(limit * 3, 3),
        filter={"source_type": source_type},
    )

    documents = deduplicate_documents(documents)
    return documents[:limit]


def retrieve_support_documents(ticket_query: str, vector_store, attached_image_document=None):
    support_documents = retrieve_by_source_type(
        ticket_query,
        vector_store,
        "support_doc",
        SOURCE_LIMITS["support_doc"],
    )

    if attached_image_document is not None:
        image_query = attached_image_document.page_content

        additional_support_documents = retrieve_by_source_type(
            image_query,
            vector_store,
            "support_doc",
            SOURCE_LIMITS["support_doc"],
        )

        support_documents = deduplicate_documents(
            support_documents + additional_support_documents
        )

    return support_documents[:SOURCE_LIMITS["support_doc"]]


def retrieve_documents(query: str, vector_store, attached_image_document=None):
    support_documents = retrieve_support_documents(
        query,
        vector_store,
        attached_image_document=attached_image_document,
    )

    image_documents = retrieve_by_source_type(
        query,
        vector_store,
        "image_ocr",
        SOURCE_LIMITS["image_ocr"],
    )

    ticket_documents = retrieve_by_source_type(
        query,
        vector_store,
        "ticket",
        SOURCE_LIMITS["ticket"],
    )

    final_documents = support_documents + image_documents + ticket_documents
    final_documents = deduplicate_documents(final_documents)

    return final_documents[:TOP_K]
