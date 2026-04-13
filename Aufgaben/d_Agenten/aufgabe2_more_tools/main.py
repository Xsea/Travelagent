"""Aufgabe 2 — Mehr Tools.

Ziel: Die Chat-Schleife aus Aufgabe 1 ist fertig. Jetzt registriert ihr drei
weitere Tools (list_hotels, give_hotel_information, book_hotel) und probiert
einen mehrschrittigen Chat aus.

Run:
    python -m Aufgaben.d_Agenten.aufgabe2_more_tools.main

Try:
    "Which hotels are on Mars?"
    "Book me Hellas Basin Haven from 2027-05-19 to 2027-05-21"
Type 'quit' to exit.
"""
import json

from openai import AzureOpenAI

from Aufgaben.d_Agenten.tools import (
    calculate_hotel_cost,
    # TODO: importiert hier list_hotels, give_hotel_information, book_hotel
)
from Aufgaben.d_Agenten.tools_description import (
    calculate_hotel_cost_tool_description,
    # TODO: importiert hier die passenden *_description Schemas
)

client = AzureOpenAI()

# TODO: ergänzt tool_map und tools mit den drei neuen Tools.
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

        for _ in range(10):
            completion = client.chat.completions.create(
                model="gpt-5.4-mini",
                tools=tools,
                messages=messages,
            )
            choice = completion.choices[0]
            messages.append(choice.message)

            if choice.finish_reason != "tool_calls":
                print(f"Agent: {choice.message.content}\n")
                break

            for tool_call in choice.message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                try:
                    result = tool_map[name](**args)
                except Exception as err:
                    result = f"error: {err}"
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
        else:
            print("Agent: (didn't finish in 10 steps)\n")


if __name__ == "__main__":
    chat()
