from fastapi import FastAPI
from ollama import Client # Tool to talk to Ollama running in Docker
from fastapi import Body

app = FastAPI() # Create my web application

# localhost = your own computer
# 11434     = Ollama running port number  : -> this line says: Hey! Connect to Ollama which is running on my computer at port 11434
client = Client( 
    host='http://localhost:11434',
)

client.pull('gemma3:1b') # Download Gemma 1B model from Ollama if not already downloaded

@app.post("/chat")
def chat(message: str = Body(..., description="Chat Message")): # Body(...) = Required field ✅
    response  = client.chat(model="gemma3:1b", messages=[
        {"role": "user", "content" : message}
    ])

    # Send AI's reply back to whoever called our /chat API"
    return response['message']['content']


# uvicorn : server that runs the API (Similar to "Nodemon" in node.js)
# command : uvicorn main:app --reload.
# Explanation : 
# main → filename
# app → FastAPI object
# --reload → auto restart when code changes



### Big Picture - How Everything Works Together:
# User calls your API
# http://localhost:8000/chat
#          ↓
# FastAPI receives the request
#          ↓
# FastAPI asks Ollama at port 11434 through client.chat() func
# "Hey send this message to Gemma AI"
#          ↓
# Ollama runs Gemma model
# inside Docker container
#          ↓
# Gemma thinks and replies
#          ↓
# Reply goes back to FastAPI
#          ↓
# FastAPI send