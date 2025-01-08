from openai import OpenAI

client = OpenAI()

assistantMessage = "How can I help you?"
# the chat history - you need to fill it
messages = []
while True:
    # accepts user input
    userRequest = str(input(assistantMessage + "\n"))
    # exit
    if userRequest == "thanks":
        break

    # this sends the request to the llm - answer you can find in the completionRequest
    completionResponse = client.chat.completions.create(
        model="gpt-4o-mini",
        )

    # things that need to be done: write a system
    # fill the messages array so that the complete chat history is there and give it to the llm
    # update the assistant message, so that the user can see what the LLM answered
