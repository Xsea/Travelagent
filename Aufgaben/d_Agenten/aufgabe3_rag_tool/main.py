"""Aufgabe 3 — RAG als Tool.

Ziel: Macht die RAG-Funktion aus dem RAG-Block (give_tourist_information_space)
zu einem weiteren Tool. Jetzt kann derselbe Agent allgemeine Reisefragen
beantworten UND Hotels buchen — in einer einzigen Konversation.

Run:
    python -m Aufgaben.d_Agenten.aufgabe3_rag_tool.main

Try:
    "What's there to see on Mars?"
    "Which hotels are on Mars?"
    "Book me one for 2027-05-19 to 2027-05-21"
Type 'quit' to exit.
"""
import json

from openai import AzureOpenAI

from Aufgaben.d_Agenten.tools import (
    book_hotel,
    calculate_hotel_cost,
    give_hotel_information,
    list_hotels,
    # TODO: importiert give_tourist_information_space
)
from Aufgaben.d_Agenten.tools_description import (
    book_hotel_description,
    calculate_hotel_cost_tool_description,
    give_hotel_information_description,
    list_hotels_description,
    # TODO: importiert give_tourist_information_space_description
)

client = AzureOpenAI()

# TODO: ergänzt tool_map und tools um den RAG-Eintrag.
tool_map = {
    "calculate_hotel_cost": calculate_hotel_cost,
    "list_hotels": list_hotels,
    "give_hotel_information": give_hotel_information,
    "book_hotel": book_hotel,
}

tools = [
    calculate_hotel_cost_tool_description,
    list_hotels_description,
    give_hotel_information_description,
    book_hotel_description,
]

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
