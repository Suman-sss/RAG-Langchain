# Level 1: Enterprise Knowledge Assistant

## Overview

This project is a grounded enterprise knowledge assistant built with LangChain and Ollama. It answers internal business questions using approved enterprise documents and image-derived knowledge sources.

The solution is designed as a local-first, zero-cost RAG system that demonstrates strong architectural foundations for enterprise AI.

## Business Problem

Employees often search across multiple internal documents such as onboarding guides, IT access policies, HR rules, and workflow references. This leads to delays, inconsistent answers, and unnecessary dependency on support teams.

## Solution

The assistant retrieves relevant knowledge from enterprise text documents and image-derived descriptions, then generates a grounded answer using only the retrieved evidence.

## Key Features

- enterprise document ingestion
- image-description ingestion for multimodal-ready retrieval
- chunking for retrieval-friendly knowledge units
- semantic search with embeddings
- local vector store using Chroma
- grounded answer generation with source citation
- refusal behavior when evidence is insufficient
- modular code structure for maintainability

## Architecture Summary

1. Load enterprise text and image-derived documents
2. Split them into chunks
3. Generate embeddings for each chunk
4. Store embeddings in a local Chroma vector database
5. Retrieve the most relevant chunks for a user query
6. Build a constrained prompt with retrieved evidence
7. Generate a source-backed answer using Ollama

## Tech Stack

- Python
- LangChain
- Ollama
- Chroma
- python-dotenv

## Sample Questions

- What should a new employee receive in the first week?
- Where is the IT service desk located?
- What happens if laptop allocation fails during onboarding?
- When should travel expenses be submitted?

## Learning Outcomes

This level teaches:

- RAG fundamentals
- document ingestion
- chunking strategy
- embeddings and semantic retrieval
- vector database basics
- grounded prompting
- multimodal-ready document handling
- enterprise-oriented modular design

## Run

```bash
python -m app.main
