# Travelagent

A workshop on building a Travel Agent with the Azure OpenAI API: function calling, RAG, and agent loops.

## Getting started

This guide sets everything up for the workshop day. At the end you'll run a small smoke-test script that uses vector search and an LLM call. If it succeeds, you're ready.

### 1. Git checkout

Clone this repository and `cd` into the project root (the folder containing this `README.md`).

### 2. Set the API key

We use the Azure OpenAI API for LLM inference. Use the API key sent to you via email.

#### Mac/Linux

```bash
export AZURE_OPENAI_API_KEY=the_api_key_here
export AZURE_OPENAI_ENDPOINT=https://m3-2026-conference-workshop.cognitiveservices.azure.com
export OPENAI_API_VERSION=2025-04-01-preview
```

#### Windows

```bash
setx AZURE_OPENAI_API_KEY "the_api_key_here"
setx AZURE_OPENAI_ENDPOINT "https://m3-2026-conference-workshop.cognitiveservices.azure.com/"
setx OPENAI_API_VERSION "2025-04-01-preview"
```

### 3. Python environment

Python 3.11+ is recommended. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate            # Linux/Mac
.venv\Scripts\activate.bat           # Windows
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the smoke test

```bash
python system_check.py
```

When prompted, type `Tell me about Mars!`. If you get a Mars travel response, you're ready for the workshop.


## Workshop structure

Exercises live under `Aufgaben/`, with reference solutions under `Solutions/`.

| Block | Folder | What you'll build |
|-------|--------|-------------------|
| Function Calling | `b_Function Calling/` | Declare a tool, dispatch its call, return the result to the LLM |
| RAG | `c_RAG/` | Vectorize a query, find the closest chunks in `travel.db`, ground the LLM's answer |
| Agents | `d_Agenten/` | Build a tool-calling agent loop, then grow it step by step |

The agent block is split into four progressive exercises that all build on the same loop:

1. `aufgabe1_loop/` — write the minimal agent loop with one tool
2. `aufgabe2_more_tools/` — register the hotel tools, watch the agent compose them
3. `aufgabe3_rag_tool/` — add the RAG retrieval as a tool — agent now answers travel questions and books trips
4. `aufgabe4_planning/` — add a planning instruction to the system prompt and compare behavior

Run any exercise from the project root, e.g.:

```bash
python -m Solutions.d_Agenten.aufgabe1_loop.main
```

---

## Rebuilding `travel.db` (only if you want to)

`travel.db` is committed to the repo, so you don't need to do this. If you want to re-seed it (e.g. to add new hotels or destinations), run:

```bash
python -m SetupFunctionsContainer.fillDatabase
```

This re-vectorizes everything in `Space Destinations/` using `text-embedding-3-large` and rebuilds the hotels and availabilities tables.
