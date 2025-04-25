def next_step(plan, executed_steps, chat_history, tools):
    ###########
    # Create a request that takes the plan and executed steps and compares them to determine the next step
    # Do not worry about executed steps too much for now. Just pass it as an additional system message)
    # let the LLM answer in a given json format,
    # this gives you  more control how the answer looks like and can manipulate it
    # the JSON should contain following parameters:
        # 1. chainOfThoughts (as a first parameter for the llm to think)
        # 2. nextStep: (the determined next step - this is the interesting part which will be used to determine the tool
        # 3. finish: a boolean, only true if the agent determines the task to be finished and then can be used to break the loop
    # The output we call "next_step"
    ###########

## TODO add dummy execution