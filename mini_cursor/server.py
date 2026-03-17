import json
import os
import subprocess
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
app = FastAPI()

# ==========================================
# 1. DEFINE OUR CURSOR-STYLE TOOLS
# ==========================================

def run_command(command: str):
    try:
        # Added timeout so the agent doesn't freeze on commands like `ping`
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

def read_url(url: str):
    try:
        # Fetch web page and extract only text (to save tokens!)
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True) # Get all text from all tags with spaces, and trim whitespace
        return text[:8000] + "... [TRUNCATED]" # Prevent breaking token limits by allowing max 3000 words
    except Exception as e:
        return f"Failed to read URL: {str(e)}"

def explore_files(path: str = "."):
    try:
        files = os.listdir(path)
        return "\n".join(files) if files else "Directory is empty."
    except Exception as e:
        return f"Error reading directory: {str(e)}"

def read_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(args_json: str):
    # Because writing a file requires 2 arguments (filepath & content), 
    # we force the LLM to pass a JSON string as the single `input` parameter.
    try:
        args = json.loads(args_json)
        with open(args["filepath"], "w", encoding="utf-8") as f:
            f.write(args["content"])
        return f"Successfully wrote to {args['filepath']}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

available_tools = {
    "run_command": {"fn": run_command, "description": "Execute any shell command. Input: command string."},
    "read_url": {"fn": read_url, "description": "Fetch text content from a web URL. Input: url string."},
    "explore_files": {"fn": explore_files, "description": "List files in a directory. Input: directory path (default '.')."},
    "read_file": {"fn": read_file, "description": "Read file contents. Input: file path string."},
    "write_file": {"fn": write_file, "description": 'Write to file. Input MUST be a JSON string like: {"filepath": "doc.txt", "content": "hello"}'}
}

tools_description = "\n".join(f"- {name}: {tool['description']}" for name, tool in available_tools.items())

# ==========================================
# 2. DEFINE SYSTEM PROMPT & API ENDPOINT
# ==========================================

system_prompt = f"""
You are an elite Cursor-style AI Assistant operating in a terminal.
You have the power to explore the file system, read/write files, execute commands, and browse the web.
You operate strictly on a start, plan, action, observe mode loop.

Rules:
- Follow the Output JSON Format strictly.
- Execute ONE step at a time!

Output JSON Format:
{{
  "step": "plan" | "action" | "output", 
  "content": "your thought process or final answer",
  "function": "tool name (if action)",
  "input" : "input for the function"
}}

Available Tools: 
{tools_description}
"""

# Pydantic model
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_with_agent(req: ChatRequest):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.query}
    ]
    
    # We will store what the AI is "doing" in this array to send back to the CLI
    action_logs = []
    
    # The AI Thinking Loop!
    for _ in range(15): # Limiting to 15 iterations so it doesn't loop infinitely
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using modern standard models
            response_format={"type": "json_object"},
            messages=messages
        )
        
        parsed = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed)})
        
        step = parsed.get("step")
        
        if step == "plan":
            action_logs.append(f"🧠 Plan: {parsed.get('content')}")
            
        elif step == "action":
            func_name, func_input = parsed.get("function"), parsed.get("input")
            action_logs.append(f"⚙️ Action: Using tool `{func_name}`")
            
            tool = available_tools.get(func_name)
            if tool:
                output = tool["fn"](func_input)
                # Feed the observation back to the LLM
                observation = {"step": "observe", "output": output}
                messages.append({"role": "assistant", "content": json.dumps(observation)})
                # Truncate logs so the CLI doesn't flood the frontend
                action_logs.append(f"👀 Observe: {str(output)[:150]}...") 
            else:
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": "Tool not found"})})
                
        elif step == "output":
            # The agent figured out the answer! Break the loop and return everything.
            return {"logs": action_logs, "final_answer": parsed.get("content")}
            
    return {"logs": action_logs, "final_answer": "Agent got confused and stopped thinking."}
