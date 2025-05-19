from openai import AzureOpenAI
from Aufgaben.d_Agenten.tools_description import tool_belt


client = AzureOpenAI()

def determine_tool(next_step, tools):
    # use the given string to let an llm decide which tools to use
    # return the choices[0].message.tool_calls[0] object
    completion_tool = client.chat.completions.create(
        model="gpt-4o-mini",
        tools=tools,
        tool_choice='required',
        messages=[
            {"role": "system",
             "content": """"""},
            {
                "role": "assistant",
                "content": next_step
                }
            ]
        )
    return completion_tool.choices[0]

if __name__ == "__main__":
    print(determine_tool("calculate the costs for a hotel with checkin date 27.03.2024, checkout date 10.04.2024 and a nightly cost of 235", tool_belt))
