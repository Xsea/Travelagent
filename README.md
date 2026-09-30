# Travelagent

A workshop on building a Travel Agent with the Azure OpenAI API: function calling, RAG, and agent loops.

## Getting started

This guide sets everything up for the workshop day. At the end you'll run a small smoke-test script that uses vector search and an LLM call. If it succeeds, you're ready.

### 1. Git checkout

Clone this repository and `cd` into the project root (the folder containing this `README.md`).

### 2. Configure the API connection

We use the OpenAI API for LLM inference. Create a local `.env` file from the
provided template, then add the API key sent to you via email:

#### Mac/Linux

```bash
cp .env.example .env
```

#### Windows

```bash
copy .env.example .env
```

Set `OPENAI_API_KEY` in `.env`. `OPENAI_BASE_URL` is preconfigured in the template.

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
