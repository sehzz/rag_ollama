# Porsche 911 Engineering Dossier — Local RAG CLI

A lightweight, fully local Retrieval-Augmented Generation (RAG) command-line assistant built with **LangChain**, **FAISS**, and **Ollama**. It indexes PDF engineering monographs stored in `data/` and answers technical queries strictly grounded in the retrieved document context.

> **⚠️ Synthetic Test Corpus Disclaimer**
> All PDF documents inside `data/` (`porsche_911_rag_benchmark_monograph.pdf`, `porsche_911_aero_cfd_dossier.pdf`, and `porsche_911_wheel_brake_metallurgy.pdf`) were **synthetically generated using AI** specifically for benchmarking and evaluating Retrieval-Augmented Generation (RAG) pipelines. While grounded in real Porsche 911 architectural history, fictionalized entities, bespoke build specifications (such as *Commission No. SG-774-BLK / Project Nachtgrau*), telemetry logs, and diagnostic tables were intentionally introduced to test single-hop retrieval, table parsing, multi-hop synthesis, and hallucination resistance. **These files are not official Porsche AG technical documentation.**
---

## Architecture & Pipeline Overview

```text
PDF Files (data/)
      │
      ▼  PyPDFLoader
Raw Document Pages
      │
      ▼  RecursiveCharacterTextSplitter (chunk_size=500, overlap=150)
Overlapping Text Chunks
      │
      ▼  OllamaEmbeddings (bge-m3)
Dense Vector Index (FAISS: "porche_911_investigations")
      │
      ▼  Top-K Similarity Search (k=5)
Retrieved Context + In-Memory Chat History
      │
      ▼  ChatOllama (qwen2.5:1.5b) with Strict Grounding Prompt
Grounded CLI Response
```

---

## Prerequisites

Python 3.10+
Ollama installed and running locally (ollama serve)
Required Ollama Models:
```bash
ollama pull bge-m3
ollama pull qwen2.5:1.5b
```

---

## Installation

Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required Python dependencies:
```bash
pip install langchain-community langchain-text-splitters langchain-ollama faiss-cpu pypdf
````

---

## Project Structure
```text
.
├── data/                         
│   ├── porsche_911_aero_cfd_dossier.pdf
│   ├── porsche_911_rag_benchmark_monograph.pdf
│   └── porsche_911_wheel_brake_metallurgy.pdf
├── porche_911_investigations/
├── main.py
└── README.md

```

---

## Example session:
```text
Question: What is the paint code and official German designation for the Slate Grey finish on Commission No. SG-774-BLK?
================================================================================
The Slate Grey finish on Commission No. SG-774-BLK has Paint Code 615 and is officially designated as "Schiefergrau".
================================================================================
Question: exit
```
