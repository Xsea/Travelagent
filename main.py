from openai import OpenAI

client = OpenAI()

assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a traveling agent, responsible for helping people planning their vacations.
             Users will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays
             """}]
while True:
    userRequest = str(input(assistantMessage + "\n"))
    if userRequest == "thanks":
        break

    messages.append({"role": "user", "content": userRequest})
    # read user input and devise a plan on how to solve it
    completionRequest = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= messages
        )

    llm_answer = completionRequest.choices[0].message
    messages.append(llm_answer)
    assistantMessage = llm_answer.content
