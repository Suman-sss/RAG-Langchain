# Enterprise Operations Intelligence Platform

This repository is a staged, architecture-first learning project for building enterprise-grade RAG, multimodal retrieval, and agentic AI systems with a local-first and cost-conscious approach.

The project is intentionally structured like a real enterprise AI program instead of a collection of disconnected demos. Each level introduces a meaningful business use case, a stronger architecture, and a more production-minded way of thinking.

## Current Status

What has been built so far:

1. `Level 1: Enterprise Knowledge Assistant`
- working LangChain-based RAG pipeline
- local Ollama generation and embeddings
- Chroma vector store
- source-grounded answers
- modular code split into config, loaders, splitter, embeddings, vector store, retriever, prompt, chain, and main orchestration

2. `Level 2: Multimodal Support Triage Copilot`
- working intermediate multimodal pipeline
- ticket ingestion
- support document ingestion
- raw image ingestion
- OCR extraction using Tesseract
- unified vector store across support docs, ticket text, and OCR-derived text
- issue classification
- structured triage recommendation generation
- baseline output evaluation against expected results

3. `Level 3: Agentic Incident Resolution Orchestrator`
- not implemented yet
- planned for later evolution into workflow-oriented and LangGraph-based orchestration

## Why This Project Exists

The goal of this repository is not only to "make something work."
It is to learn how enterprise AI systems are actually designed:

- how data is organized
- how retrieval works in practice
- how multimodal pipelines bridge images into text retrieval
- how classification and recommendation differ from simple Q&A
- how evaluation should be introduced early
- how to build in small, meaningful architecture layers

This repo is especially designed to prepare for:

- enterprise client discussions
- AI/ML system design rounds
- RAG and multimodal interview questions
- production-minded project explanations

## Project Structure

```text
rag-langchain/
├── README.md
├── docs/
│   ├── platform-overview.md
│   └── architecture-level-1.md
├── level_1_knowledge_assistant/
├── level_2_multimodal_triage/
├── level_3_incident_orchestrator/
├── shared/
└── infra/
```

This structure is intentional.
It separates:

- platform-level documentation
- level-specific implementations
- shared reusable assets
- future infrastructure concerns

That makes the repository look and behave more like a professional project.

## Level 1: Enterprise Knowledge Assistant

### Business Use Case

Employees often need answers from:

- onboarding guides
- HR policies
- IT access documents
- reimbursement rules
- internal process references

Instead of searching manually through multiple documents, Level 1 provides a grounded knowledge assistant.

### What We Built

Level 1 uses:

- LangChain
- Ollama
- Chroma
- local text documents
- image-derived text descriptions

The pipeline:

```text
Documents + Image Descriptions
-> Loaders
-> Chunking
-> Embeddings
-> Chroma Vector Store
-> Retriever
-> Prompt
-> LLM
-> Grounded Answer with Sources
```

### What It Teaches

- RAG fundamentals
- document ingestion
- chunking
- embeddings
- vector store usage
- prompt grounding
- source citation
- why retrieval quality matters

### Important Design Choice

Level 1 used image-description text files rather than raw images.

Why?

Because Level 1 was meant to teach the retrieval architecture first, without introducing OCR complexity too early.

That let us understand the basic RAG pipeline cleanly before making it truly multimodal.

## Level 2: Multimodal Support Triage Copilot

### Business Use Case

Support teams often work with mixed evidence:

- support tickets
- SOPs and runbooks
- screenshots
- dashboard alerts
- operational guidance

A good support AI system should not only answer questions.
It should:

- identify the issue type
- retrieve relevant support knowledge
- use image evidence
- recommend the next operational step

That is what Level 2 introduces.

### Data Used in Level 2

Level 2 currently contains:

1. `Ticket Files`
- VPN login issue
- MFA reset issue
- account locked issue
- laptop provisioning delay
- repository access denied

2. `Support Documents`
- VPN troubleshooting guide
- MFA reset SOP
- account recovery runbook
- device provisioning workflow
- access escalation matrix

3. `Raw Image Files`
- VPN error screenshot
- MFA setup failure screenshot
- account locked dashboard screenshot
- laptop provisioning queue screenshot

4. `Expected Outputs`
- reference triage outputs used for baseline evaluation

### What We Built

Level 2 pipeline:

```text
Ticket Files + Support Docs + Raw Images
-> Text Loaders
-> OCR Image Processing
-> Unified Document Pool
-> Chunking
-> Embeddings
-> Chroma Vector Store
-> Retriever
-> Issue Classification
-> Triage Prompt
-> LLM Recommendation
-> Evaluation Against Expected Output
```

### What This Means Practically

When a user enters a ticket file name like:

```text
vpn_login_issue.txt
```

the system:

1. finds the corresponding ticket content
2. classifies the issue into one category
3. retrieves semantically related evidence from the mixed corpus
4. builds a structured support context
5. generates a triage-style response:
   - issue category
   - likely cause
   - recommended next step
   - sources
6. compares the generated output with the expected output fixture

### Why This Is a Stronger Enterprise Design

This is no longer simple Q&A.

It becomes:

- workflow-driven
- multimodal
- source-aware
- evaluation-ready
- more realistic for support operations

That is why Level 2 looks much more like a mid-level or senior enterprise AI project.

## Detailed Flow of the Current Level 2 System

Below is the actual flow that is working right now.

### Step 1: Load Text Data

The system loads:

- support docs
- ticket files

These are normalized into LangChain `Document` objects.

### Step 2: Process Raw Images with OCR

The system reads real image files from the image folder and runs OCR using:

- `Pillow`
- `pytesseract`
- system-level `tesseract-ocr`

The extracted text is then converted into `Document` objects.

### Step 3: Unify the Corpus

The system combines:

- support docs
- tickets
- OCR-derived image text

into one retrieval corpus.

### Step 4: Chunk the Documents

The unified documents are chunked to improve retrieval granularity.

### Step 5: Build Embeddings and Vector Store

The chunked documents are embedded using Ollama embeddings and stored in Chroma.

### Step 6: Select a Ticket

The user enters a ticket file name such as:

```text
vpn_login_issue.txt
```

The system finds that ticket from the loaded ticket documents.

### Step 7: Classify the Issue

The ticket text is classified into one of:

- `vpn_access`
- `mfa_issue`
- `account_recovery`
- `device_provisioning`
- `repository_access`
- `unknown`

### Step 8: Retrieve Relevant Evidence

The system uses the ticket text as the retrieval query and fetches the top semantically similar chunks from the mixed corpus.

### Step 9: Generate a Triage Recommendation

The model receives:

- the predicted issue category
- the original ticket text
- the retrieved context

and returns a structured triage response.

### Step 10: Evaluate Against Expected Output

The generated result is compared with the expected output fixture for that ticket.

This gives a basic but useful baseline signal for correctness.

## Challenges Faced So Far

This section is important because real engineering projects are not only about what works. They are also about what problems appeared and how they were handled.

### 1. Challenge: Starting with a clean architecture instead of one big script

If everything is written in a single file, the project becomes hard to understand, hard to debug, and hard to explain in interviews.

#### What we did

We separated responsibilities into modules such as:

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

#### Why this was the right approach

Because it reflects how real systems are designed:

- configuration is separate
- ingestion is separate
- OCR is separate
- retrieval is separate
- classification is separate
- generation is separate
- orchestration is separate

### 2. Challenge: Handling images in a practical free-cost way

At first, Level 1 used text descriptions for image-related knowledge.

That was useful for learning but not truly multimodal.

#### What we changed

For Level 2, we moved to real raw image files and added OCR-based extraction.

#### Why this approach was chosen

We considered the broader multimodal options:

- manual image descriptions
- OCR extraction
- direct vision-model reasoning

We chose OCR because:

- it is practical for text-heavy screenshots
- it is cheaper and easier to operate locally
- it teaches a realistic enterprise workflow
- it avoids unnecessary paid dependencies

### 3. Challenge: `pytesseract` alone was not enough

This was a real runtime issue.

The Python package `pytesseract` was installed, but OCR still could not work until the system-level `tesseract-ocr` binary was installed.

#### What we did

We installed:

```bash
sudo apt install tesseract-ocr
```

#### Why this matters

This is an important practical engineering lesson:

some Python libraries are only wrappers and still depend on system tools.

### 4. Challenge: Retrieval quality in Level 2 is currently mixed

The system works end to end, but retrieval currently returns a mix of:

- relevant ticket
- semantically related tickets
- relevant support doc

instead of strongly prioritizing authoritative support knowledge.

#### What happened

For the VPN ticket test, retrieval brought back:

- the selected VPN ticket
- other semantically similar tickets
- one very relevant support guide

#### Why this happens

Because the current retrieval design uses:

- a unified vector store
- simple top-k semantic retrieval

This is a strong baseline, but not yet source-prioritized.

#### What we learned

This taught us that:

- a system can work technically
- but still need retrieval ranking improvements

#### Planned improvements

Later we can improve this with:

- metadata-aware retrieval
- source-type preference
- reranking
- hybrid retrieval

### 5. Challenge: Source citation in Level 2 is not yet ideal

The generated triage response sometimes cites only the ticket file, even when the recommendation clearly comes from a support document.

#### Why this happens

Because source attribution depends on:

- retrieval balance
- prompt clarity
- model obedience to source instructions

#### What we learned

Good RAG output depends not only on retrieval, but also on:

- context quality
- output constraints
- citation control

### 6. Challenge: Exact-match evaluation is too strict

The evaluator currently compares generated and expected output using exact match after simple normalization.

#### Why this is useful

It gives us a baseline evaluation contract.

#### Why it is limited

Two outputs can be semantically correct but still differ in wording.

#### What we plan later

We may later add:

- field-wise comparison
- softer semantic evaluation
- source-specific checks
- MLflow experiment logging

## Why the Current Design Still Makes Sense

Even with the current limitations, the project is in a strong place because:

- the system is fully modular
- Level 1 works
- Level 2 works end to end
- OCR is functioning
- classification works
- triage response generation works
- evaluation exists

That means we have a working baseline architecture.

In real engineering, building a clean baseline and then improving it step by step is better than trying to prematurely design the perfect system.

## Technologies Used So Far

- Python
- LangChain
- Ollama
- Chroma
- Tesseract OCR
- Pillow
- pytesseract
- python-dotenv
- MLflow added as a planned experiment-tracking dependency for the next evaluation stage

## Why This Repository Is Useful for Client Rounds

This repository is not positioned as a toy chatbot project.

It demonstrates:

- enterprise problem framing
- modular architecture
- retrieval-augmented generation
- multimodal ingestion through OCR
- support triage design
- structured LLM outputs
- evaluation thinking
- cost-conscious local-first engineering

This is exactly the kind of framing that makes a stronger impression in:

- client demonstrations
- architecture discussions
- AI/ML interviews
- solution design rounds

## What Is Next

The next evolution steps are likely to include:

1. better Level 2 retrieval quality
- prioritize support docs more strongly
- make retrieval more source-aware

2. stronger evaluation
- field-level comparison
- better correctness checks
- MLflow logging

3. advanced orchestration
- move into Level 3
- introduce more agentic workflow design
- eventually bring in LangGraph where it adds real value

## Important Note

This repository is being built incrementally and committed in stages on purpose.

The intention is:

- build
- understand
- evaluate
- improve
- commit each meaningful stage

That means the commit history itself reflects the engineering journey, not just the final result.
