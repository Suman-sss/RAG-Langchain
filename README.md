# Enterprise Operations Intelligence Platform

This repository is an architecture-first learning project for building enterprise-grade RAG systems with a local-first and cost-conscious stack.

Right now this repo contains two completed stages:

1. `Level 1: Enterprise Knowledge Assistant`
2. `Level 2: Multimodal Support Triage Copilot`

The previously planned Level 3 placeholder has been intentionally removed from this repository. The next advanced project will be built as a separate repository so this repo stays clean and easy to understand as a two-level learning journey.

## Current Status

### Level 1: Enterprise Knowledge Assistant

Built and working:

- LangChain-based RAG pipeline
- Ollama for generation and embeddings
- Chroma vector store
- source-grounded answers
- modular code split into configuration, ingestion, splitting, embeddings, vector store, retrieval, prompting, chaining, and orchestration

### Level 2: Multimodal Support Triage Copilot

Built and working:

- ticket ingestion
- support-document ingestion
- raw image ingestion
- OCR extraction using Tesseract
- multimodal retrieval across tickets, support docs, and OCR-derived text
- issue classification
- structured triage response generation
- deterministic source attribution
- field-wise and overlap-aware evaluation

## Why This Repository Exists

The goal of this repository is not just to make a demo work.

It is meant to show how enterprise AI systems are built step by step:

- data organization
- modular architecture
- retrieval design
- source grounding
- multimodal evidence handling
- workflow-oriented output design
- evaluation maturity

This repo is especially useful for:

- enterprise client discussions
- AI/ML interviews
- solution architecture rounds
- explaining RAG decisions clearly with real code

## Repository Structure

```text
rag-langchain/
├── README.md
├── docs/
│   ├── architecture-level-1.md
│   └── platform-overview.md
├── level_1_knowledge_assistant/
└── level_2_multimodal_triage/
```

This structure is intentional.

- `docs/` holds platform and architecture notes
- `level_1_knowledge_assistant/` holds the foundational RAG project
- `level_2_multimodal_triage/` holds the stronger multimodal and workflow-oriented project

## Level 1: Enterprise Knowledge Assistant

### Business Use Case

Employees often need answers from:

- onboarding guides
- HR policies
- IT access guides
- reimbursement rules
- internal knowledge documents

Instead of manually searching through files, Level 1 provides a grounded enterprise knowledge assistant.

### Level 1 Architecture

```text
Documents + Image Descriptions
-> Loaders
-> Chunking
-> Embeddings
-> Chroma Vector Store
-> Retriever
-> Prompt
-> LLM
-> Answer with Sources
```

### What Level 1 Teaches

- RAG fundamentals
- document ingestion
- chunking
- embeddings
- vector-store usage
- retrieval grounding
- prompt design basics
- source citation basics

### Important Design Choice in Level 1

Level 1 uses image-description text files rather than raw image OCR.

That was intentional.
It let us learn the retrieval pipeline first without introducing OCR complexity too early.

## Level 2: Multimodal Support Triage Copilot

### Business Use Case

Support operations rarely depend on one source of truth.
Real triage often needs:

- a support ticket
- one or more runbooks or SOPs
- a screenshot or alert image
- a recommended operational next step

Level 2 was built to reflect that reality.

This is no longer simple document Q&A.
It is a support-triage workflow with mixed evidence.

## Level 2 Data

### Ticket Files

- `vpn_login_issue.txt`
- `mfa_reset_issue.txt`
- `account_locked_ticket.txt`
- `laptop_delay_ticket.txt`
- `repo_access_denied.txt`

### Support Documents

- `vpn_troubleshooting_guide.txt`
- `mfa_reset_sop.txt`
- `account_recovery_runbook.txt`
- `device_provisioning_workflow.txt`
- `access_escalation_matrix.txt`

### Raw Images

- `vpn_login_error.bmp`
- `mfa_setup_failure.bmp`
- `account_locked_alert.bmp`
- `laptop_provisioning_queue.bmp`

### Expected Output Fixtures

- one expected triage output per ticket for baseline evaluation

## Level 2 Architecture

```text
Ticket Files + Support Docs + Raw Images
-> Text Loaders
-> OCR Image Processing
-> Unified Document Pool
-> Chunking
-> Embeddings
-> Chroma Vector Store
-> Issue Classification
-> Source-Aware Retrieval
-> Structured Triage Prompt
-> LLM Recommendation
-> Deterministic Source Normalization
-> Evaluation
```

## What Level 2 Does in Practice

When a user enters a ticket file name such as:

```text
vpn_login_issue.txt
```

the system:

1. loads the selected ticket
2. extracts the attached image name if present
3. OCRs the linked image and keeps it available as direct evidence
4. classifies the issue into a support category
5. retrieves support documents, OCR evidence, and ticket context
6. builds a structured context for the model
7. generates a triage response with:
   - issue category
   - likely cause
   - recommended next step
   - sources
8. normalizes the final `Sources:` line in application code
9. compares the result against an expected output fixture

## What We Improved During Level 2

This part is important because the current Level 2 system was not built in one shot. It improved through several deliberate architecture upgrades.

### 1. Started with a clean modular design

We split the project into modules such as:

- `config.py`
- `loaders.py`
- `image_processor.py`
- `splitter.py`
- `embeddings.py`
- `vectorstore.py`
- `retriever.py`
- `classifier.py`
- `prompt_builder.py`
- `chain.py`
- `evaluator.py`
- `main.py`

This made the project:

- easier to debug
- easier to explain
- easier to improve step by step

### 2. Moved from image descriptions to real OCR

Level 1 used text descriptions for images.
Level 2 moved to real raw image files plus OCR using:

- `Pillow`
- `pytesseract`
- system `tesseract-ocr`

This made the project meaningfully multimodal while still staying local-first and low-cost.

### 3. Learned the difference between Python wrappers and system binaries

`pytesseract` alone was not enough.
OCR only worked after installing the actual system binary:

```bash
sudo apt install tesseract-ocr
```

This was an important practical engineering lesson.

### 4. Improved retrieval beyond simple top-k similarity

The first retrieval version over-weighted tickets because ticket text naturally looks similar to other ticket text.

We then improved the system by moving through these retrieval ideas:

- simple unified retrieval
- reranking by source type
- source-specific retrieval
- support-document retrieval with stronger evidence balancing
- support-document retrieval using both ticket text and OCR text from the attached image

This made authoritative support docs much more likely to appear in the final context.

### 5. Added explicit ticket-to-image linking

Instead of only hoping retrieval would find the right OCR evidence, the system now:

- reads `Attached Image:` from the selected ticket
- finds the OCR document for that exact image
- injects that case-linked image evidence into the final context

This made the Level 2 flow much more realistic for enterprise support use cases.

### 6. Strengthened prompt quality

The prompt was iteratively improved to better control:

- grounding
- structured output
- source formatting
- complete next-step responses

This reduced output drift and made the response more operational.

### 7. Moved source attribution into application logic

Prompt-only source citation was not reliable enough.

So we introduced deterministic source handling in `main.py`.
The app now builds the final `Sources:` line using a policy-aware rule:

- include relevant support docs
- include the exact attached image source
- avoid noisy over-citation

This is a more production-style design than leaving critical metadata fields entirely to the LLM.

### 8. Upgraded evaluation from exact-match-only to richer comparison

The evaluation layer now includes:

- whole-output exact match
- normalized comparison
- field-wise comparison
- source overlap analysis

This gives a much fairer and more informative view of system quality.

## Current Level 2 Strengths

The current Level 2 system now demonstrates:

- raw image OCR
- mixed evidence ingestion
- support issue classification
- multimodal retrieval
- source-aware retrieval refinement
- exact ticket-to-image evidence linking
- deterministic source attribution
- structured triage generation
- evaluation with source coverage metrics

One representative run for `vpn_login_issue.txt` now produces:

- correct issue category
- correct expected source set
- full source overlap coverage
- a likely cause and next step that are semantically close to the reference output

## Technologies Used

- Python
- LangChain
- Ollama
- Chroma
- Tesseract OCR
- Pillow
- pytesseract
- python-dotenv

## Why This Repository Is Strong for Interviews and Client Rounds

This repository is not framed as a toy chatbot.

It demonstrates:

- enterprise problem framing
- modular design
- RAG fundamentals
- multimodal evidence handling
- workflow-oriented AI output
- grounded recommendations
- evaluation thinking
- iterative architecture improvement

That makes it easier to discuss:

- why the system was designed this way
- how retrieval quality was improved
- how OCR was integrated
- why some responsibilities were moved from prompts into code
- how evaluation matured along with the application

## Important Note on the Commit History

This repository is being built in stages on purpose.

The intention is:

- build
- understand
- improve
- evaluate
- commit each meaningful milestone

So the git history reflects the learning and engineering journey, not just the final state.
