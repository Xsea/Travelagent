# Travelagent

## Getting started
This getting started guide is there, to set up everything up for the workshop day. At the end, you will run a small script
that will make use of vectorization, a database call to a dockerized db, and an llm inference. If everything works, you are ready for the workshop!

### Git checkout
Please checkout this git repository and change your working directory in your terminal to the root folder of this project (it includes this readme.md)

### Create OpenAI Account and set Env Variable
(Skip step 1+2 if you already have an account and an exported API Key)

In this workshop we use the OpenAI API  for LLM inference.

If you do not have an OpenAI API Account, please create one. It should start you with a 5$ starting budget, 
which is enough for the workshop: Create OpenAi API account: https://platform.openai.com/ (Sign Up button is on the top right)

After creating the account, you need to set the API Key as an ENV variable on your computer. 
    You can create a new account under "Your Profile" -> "API Keys". Then export the key the following way:

#### Mac/Linux:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

#### Windows: 
```bash
setx OPENAI_API_KEY "your_api_key_here"
```
### Python Setup
It is strongly recommended to use virtual environments for working on 
python projects, as this the only way for package managment. We assume you have installed python3 with the current version. 
#### Create the venv
```bash
python3 -m venv travel_agent_env
```
#### Activate the venv

#### Linux/Mac: 
```bash
source travel_agent_env/bin/activate
```

#### Windows: 
```bash
travel_agent_env/bin/activate.bat
```
What this does is, that now all packages (dependencies) you install will only be valid for this venv.

### Install necessary python dependencies
```bash
pip install requirements.txt
```

### Install Podman
(If you know your way around docker, can troubleshoot it yourself and have it installed, you can skip this step and use docker) 

Podman is a free alternative to docker. We us it for our vectorDB. 

Follow the instructions here: https://podman.io/docs/installation, until you have run the commands ```podman machine init``` AND ```podman machine start``` (except Linux users, who can stop after downloading the cli)

### Building the image
Now we that we have setup podman we can start to build our own container.
Change your working directory: 
```bash 
cd PGVectorCointainer
``` 
and 
```bash 
podman build -t postgres_container_image .
``` 
to build the image

### Run the container and the test script

Start the container, inside is our data we will use for RAG:
```bash
podman run -d -p 5432:5432 --name postgres_container postgres_container_image
```
Now everything should be setup! So you can finally run our start script and verify everything works: 
```bash
cd ..
```
```bash
python3 main.py
```
and answer the Terminals question with "Tell me about Mars!". If you get some information about hotels and cities on Mars,
    instead of the explanation of the red planet, everything works perfectly and you are ready to go. If not, please reach out!