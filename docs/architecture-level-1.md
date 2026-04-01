# Level 1 Architecture

## Project
Enterprise Knowledge Assistant

## Business Problem
Employees lose time searching for internal knowledge across onboarding guides, policies, and process documents.

## Solution Summary
Use a RAG-based assistant to answer only from approved enterprise knowledge, with source-backed responses.

## High-Level Architecture

User Question
-> Loader Layer
-> Chunking Layer
-> Embedding Layer
-> Local Vector Store
-> Retriever
-> Prompt Construction
-> LLM Generation
-> Grounded Answer With Sources

## Multimodal Strategy
Images are represented through descriptive text or OCR-derived text and indexed alongside document content.

## Why This Matters
This provides a practical, enterprise-friendly starting point that is explainable and easy to extend.
