"""Centralized Azure OpenAI access for the workshop."""

from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().with_name(".env"))

CHAT_MODEL = "gpt-5.6-luna"
EMBEDDING_MODEL = "text-embedding-3-large"

client = OpenAI()


def complete(
    *,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    tool_choice: Literal["none", "auto", "required"] | None = None,
):
    """Create a chat completion with the workshop's configured LLM."""
    request = {"model": CHAT_MODEL, "messages": messages}
    if tools is not None:
        request["tools"] = tools
    if tool_choice is not None:
        request["tool_choice"] = tool_choice
    return client.chat.completions.create(**request)


def embed(inputs: list[str]) -> list[float]:
    """Create an embedding with the workshop's configured embedding model."""
    return client.embeddings.create(input=inputs, model=EMBEDDING_MODEL).data[0].embedding
