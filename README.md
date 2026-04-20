# Travelagent

## Getting started

This getting started guide is there, to set up everything up for the workshop day. At the end, you will run a small script that will make use of vectorization, a database call, and a LLM inference. If everything works, you are ready for the workshop!


### Git checkout

Please checkout this git repository and change your working directory in your terminal to the root folder of this project (it includes this `README.md`)

### Export the provided API-Key

In this workshop we use the Azure OpenAI API for LLM inference.
Please use the API-Key send to you via E-Mail.

#### Mac/Linux:
```bash
export AZURE_OPENAI_API_KEY=the_api_key_here
export AZURE_OPENAI_ENDPOINT=https://2025-m3-workshop-ragenten.openai.azure.com/
export OPENAI_API_VERSION=2025-01-01-preview
```

#### Windows: 

```bash
setx AZURE_OPENAI_API_KEY "the_api_key_here"
setx AZURE_OPENAI_ENDPOINT "https://2025-m3-workshop-ragenten.openai.azure.com/"
setx OPENAI_API_VERSION "2025-01-01-preview"
```

### Python Setup

We assume the usage of virtual environments for working on this (and other) python projects. We assume you have installed python3 with an up2date version. (On Windows, write `python` instead of `python3`.)


#### Create the venv

```bash
python3 -m venv .venv
```


#### Activate the venv

In that shell / terminal session all the installed packages are now available.

#### Linux/Mac: 

```bash
source .venv/bin/activate
```


#### Windows: 

```bash
Set-ExecutionPolicy Unrestricted -Scope Process   # Allows script execution for this session
.venv/Scripts/activate.bat
```


### Install necessary python dependencies

```bash
pip install -r requirements.txt
```


### Verify the setup

Now everything should be setup! Run the system check script:
```bash
python3 system_check.py
```
and answer the Terminals question with "Tell me about Mars!". If you get some information about hotels and cities on Mars, instead of the explanation of the red planet, everything works perfectly and you are ready to go. If not, please reach out!
