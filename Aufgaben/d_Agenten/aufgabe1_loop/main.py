"""Aufgabe 1 — Der Agent Loop.

Ziel: Schreibt die Tool-Schleife innerhalb von chat(). Das äußere
Chat-Gerüst (User-Input lesen, Agent-Antwort drucken) ist schon da —
ihr müsst nur den Agent-Teil schreiben, der das LLM aufruft und bei
Bedarf Tools ausführt, bis das Modell eine finale Antwort gibt.

Run:
    python -m Aufgaben.d_Agenten.aufgabe1_loop.main

Type your message at the prompt. Try:
    "How much will I pay for 3 nights at a hotel that costs 120€ per night?"
Type 'quit' to exit.
"""
import json

from openai import AzureOpenAI

from Aufgaben.d_Agenten.tools import calculate_hotel_cost
from Aufgaben.d_Agenten.tools_description import calculate_hotel_cost_tool_description

client = AzureOpenAI()

# Lookup table: tool name -> python function. Wird in jeder weiteren Aufgabe ergänzt.
tool_map = {
    "calculate_hotel_cost": calculate_hotel_cost,
}

tools = [calculate_hotel_cost_tool_description]

system_prompt = (
    "You are a space travel agent. Help the user plan trips. "
    "Use the tools whenever you need a calculation or piece of data."
)


def chat():
    messages = [{"role": "system", "content": system_prompt}]
    while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() in ("quit", "exit", "bye"):
            break
        messages.append({"role": "user", "content": user_input})

        # TODO: Schreibt hier die Agent-Schleife, die innerhalb EINES User-Turns
        # so lange mit dem LLM spricht, bis keine weiteren Tool-Calls mehr kommen.
        #
        # Pseudocode:
        #   for _ in range(10):  # Sicherheitsnetz
        #       1. completion = client.chat.completions.create(
        #              model="gpt-5.4-mini", tools=tools, messages=messages)
        #       2. choice = completion.choices[0]
        #          messages.append(choice.message)    # WICHTIG: assistant-Antwort speichern
        #       3. if choice.finish_reason != "tool_calls":
        #              print(f"Agent: {choice.message.content}\n")
        #              break
        #       4. for tool_call in choice.message.tool_calls:
        #              name = tool_call.function.name
        #              args = json.loads(tool_call.function.arguments)
        #              try:
        #                  result = tool_map[name](**args)
        #              except Exception as err:
        #                  result = f"error: {err}"
        #              messages.append({
        #                  "role": "tool",
        #                  "tool_call_id": tool_call.id,
        #                  "content": str(result),
        #              })
        #
        # Tipp: Jeder tool_call braucht GENAU eine zugehörige tool-Message
        #       mit derselben tool_call_id, sonst meckert die API.
        raise NotImplementedError("Aufgabe 1: write the agent loop")


if __name__ == "__main__":
    chat()
