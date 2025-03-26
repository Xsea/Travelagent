# Travelagent

## Getting started
This getting started guide is there, to set up everything up for the workshop day. At the end, you will run a small script
that will make use of vectorization, a database call to a dockerized db, and an llm inference. If everything works, you are ready for the workshop!

0. check out this git repository.

The first thing we ask of you, is to create an OpenAI API account, as our material uses it for LLM inference.
(Skip step 1+2 if you already have an account and an exported API Key)
1. If you do not have an OpenAI API Account, please create one. It should start you with a 5$ starting budget, 
    which is enough for the workshop: Create OpenAi API account: https://platform.openai.com/ (Sign Up button is on the top right)
2. After creating the account, you need to set the API Key as an ENV variable on your computer. 
    You can create a new account under "Your Profile" -> "API Keys". Then export the key the following way:
   Mac/Linux: "export OPENAI_API_KEY="your_api_key_here""
   Windows: "setx OPENAI_API_KEY "your_api_key_here""
3. Now we start with your python setup: It is strongly recommended to use virtual environments for working on 
   python projects, as this the only way for package managment. We assume you have installed python3. 
   Now run: "python3 -m venv travel_agent_env"
4. After setting up the venv, you can activate it like this: "source travel_agent_env/bin/activate"
    What this does is, that now all packages (dependencies) you install will only be valid for this venv.
5. Now we install the required packages needed for the project, the openai package to access the OpenAI API more easily
   and the psycopg2 package, used to talk to our pgVector DB for the RAG part. 
   Run: "pip install openai"
   And: "pip install psycopg2"
6. Next step is to download podman, a free alternative to docker. Follow the instructions here: https://podman.io/docs/installation
   until you have run the commands "podman machine init" AND "podman machine start"
7. Now we that we have setup podman we can start run our own container. After checking out this git repository, 
   change your working directory to "PGVectorCointainer" and run: "podman build -t postgres_container_image ." to build the image
8. After the image is build, run: "podman run -d -p 5432:5432 --name postgres_container postgres_container_image"
9. Now everything should be setup! So you can finally run our start script and verify everything works: Go to the folder with the main.py file
   and run "python3 main.py" and answer the Terminals question with "Tell me about Mars!". If you get some information about hotels and cities on Mars,
    instead of the explanation of the red planet, everything works perfectly and you are ready to go. If not, please reach out!