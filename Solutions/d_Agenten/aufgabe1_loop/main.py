"""Aufgabe 1 — Der Agent Loop (Lösung).

Run:
    python -m Solutions.d_Agenten.aufgabe1_loop.main

Type your message at the prompt. Try:
    "How much will I pay for 3 nights at a hotel that costs 120€ per night?"
Type 'quit' to exit.
"""
import json

from openai import AzureOpenAI

from Solutions.d_Agenten.tools import calculate_hotel_cost
from Solutions.d_Agenten.tools_description import calculate_hotel_cost_tool_description

client = AzureOpenAI()

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
