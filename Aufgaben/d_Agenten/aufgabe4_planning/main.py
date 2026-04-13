"""Aufgabe 4 — Planning (Stretch).

Ziel: Erweitert den system_prompt so, dass das Modell ZUERST einen Plan
schreibt (mit Schritten und kurzer Begründung) und DANN die Tools aufruft.
Vergleicht das Verhalten mit Aufgabe 3 bei mehrstufigen Anfragen.

Tipp: Es reicht, dem Modell im System Prompt zu sagen, dass es vor jedem
Tool-Call einen kurzen Plan ausgeben soll. Kein zusätzlicher API-Call,
kein eigener "next_step" Schritt nötig.

Run:
    python -m Aufgaben.d_Agenten.aufgabe4_planning.main

Try a multi-step request:
    "I want a 4-day trip to Mars in May 2027. What sights are there,
     which family hotel would you recommend, and what would the stay cost?"
Type 'quit' to exit.
"""
import json

from openai import AzureOpenAI

from Aufgaben.d_Agenten.tools import (
    book_hotel,
    calculate_hotel_cost,
    give_hotel_information,
    give_tourist_information_space,
    list_hotels,
)
from Aufgaben.d_Agenten.tools_description import (
    book_hotel_description,
    calculate_hotel_cost_tool_description,
    give_hotel_information_description,
    give_tourist_information_space_description,
    list_hotels_description,
)

client = AzureOpenAI()

tool_map = {
    "calculate_hotel_cost": calculate_hotel_cost,
    "list_hotels": list_hotels,
    "give_hotel_information": give_hotel_information,
    "book_hotel": book_hotel,
    "give_tourist_information_space": give_tourist_information_space,
}

tools = [
    calculate_hotel_cost_tool_description,
    list_hotels_description,
    give_hotel_information_description,
    book_hotel_description,
    give_tourist_information_space_description,
]

# TODO: erweitert den system_prompt um eine Planungs-Anweisung.
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
