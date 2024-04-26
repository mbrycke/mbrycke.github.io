---
title: Self-hosting RAG part 1
date: 2024-04-25
categories: [deep learning,rag]
tags: [vector database, embeddings, rag, self-hosting, docker, postgresql, pgvector]
---
    
## Introduction
RAG (Retrieval Augmented Generation) is the idea to store data in reasonable small chunks in a vector database (with embeddings). When a query is made, we tranform the query to a vector using the same embedding-model as the data was stored with. Then then retrieve the most similiar vectors (the cosine similarity), let's say the top 5. We then give the data corresponding to these vectors to a genrative language model togehter with the query, and ask the model to get the information from the given data that is most relevant to the query.

In this way we can store lots of data and query an llm about it without having a huge context window.

In this series we will outline how to self-host the RAG model. In this first part we will set up a server for the embeddings model. It will be fully functional, but very basic. For a production environment you need to add more features, like logging, error handling, security etc.

>For a production environment you need to add more features, like logging, error handling, security, better efficency, thread safe queueing of incoming requests etc.
{: .prompt-warning}


## Why self-hosting
There might be several reason, e.g. you could be handling sensitive data. There is also the fact that models evolve rapidly and you might want to have control over the models you are using, both for embedding and text generation.

## Running a server for the embeddings model
By running the model on server we don't have to load the model in memory every time we want to make a query. Sure, when we populate the database the time to load the model might be small compared to the time to populate the database, but when we want to make a query we don't want to wait for the model to load every time.

### Setting up the server
There are a bunch of backend servers for python, like flask or the very similar fastapi. We will use flask in this very basic example.

This is the structure of the project:
```
embeddings_server/
├── flask_server.py
|── requirements.txt
|── flask_app/
|   ├── __init__.py
|   ├── routes.py
```

The `flask_server.py` file is the entry point of the server. It looks like this:
```python
from flask_app import app
```

We load the model in `flask_app/__init__.py` to ensure it is loaded only once. If you have a big model you might e.g. run out of memory if the model is reloaded during upstart of the server etc.
```python
from flask import Flask
from llm2vec import LLM2Vec
import torch
from transformers import AutoTokenizer, AutoModel, AutoConfig
from peft import PeftModel

app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("McGill-NLP/LLM2Vec-Mistral-7B-Instruct-v2-mntp")
config = AutoConfig.from_pretrained("McGill-NLP/LLM2Vec-Mistral-7B-Instruct-v2-mntp", trust_remote_code=True)
model = AutoModel.from_pretrained(
    "McGill-NLP/LLM2Vec-Mistral-7B-Instruct-v2-mntp",
    trust_remote_code=True,
    config=config,
    torch_dtype=torch.bfloat16,
    device_map="cuda" if torch.cuda.is_available() else "cpu",
)
model = PeftModel.from_pretrained(model, "McGill-NLP/LLM2Vec-Mistral-7B-Instruct-v2-mntp")
l2v = LLM2Vec(model, tokenizer, pooling_mode="mean", max_length=512)

from flask_app import routes 
```

In `routes.py` we define the routes of the server. In this case we have a single route that takes a query and returns the vector of the query.
```python
from flask_app import app, l2v  
from flask import request, jsonify

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/embed', methods=['POST'])
def embed():
    content = request.json
    text_list = content['text_list']
    assert isinstance(text_list, list)
    embedding = get_embedding(text_list)
    return jsonify(embedding.tolist())

def get_embedding(text_list: list):
    return l2v.encode(text_list)
```

and the `requirements.txt` 
```
flask==3.0.3
llm2vec==0.1.4
peft==0.10.0
torch==2.2.2
transformers==4.40.0
```

### Running the server
Set up a virtual environment and install the requirements:
```bash
pip install -r requirements.txt
```

Set environment variables:
```bash
export FLASK_APP=flask_server.py # you can have the full path here so you can run the server from any directory
```
If you didn't set the full path to `flask_server.py` you have to run the server from the directory where `flask_server.py` is located with the command:
```bash
flask run
```
This server will run on `127.0.0.1:5000`. You can specify the host and port with the `--host` and `--port` flags in the `flask run` command. E.g. `flask run --host=0.0.0.0 --port=5001` 

## Calling the server
You can call the server with the following python code:
```python
import requests
api_url="http://127.0.0.1:5000/embed"

# make a post request
data = {"text_list": ["What is the capital of Island", "How many people live in Faroe Islands"]}
response = requests.post(api_url, json=data)
print(response.json())
```
You should get back a list of two vectors with the embeddings of the two queries.

Now we are ready to populate the database with the embeddings of the data we want to store. We will do this in the next part of this series (part2).
