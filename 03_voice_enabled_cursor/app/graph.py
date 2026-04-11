from typing import Annotated
import os
import requests
from bs4 import BeautifulSoup
import subprocess
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage
from langchain.chat_models import init_chat_model 
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool()
def run_command(command: str) -> str:
    """Execute any shell command. Input: command string."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

@tool
def read_url(url: str) -> str:
    """Fetch text content from a web URL. Input: url string."""
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:8000] + "... [TRUNCATED]"
    except Exception as e:
        return f"Failed to read URL: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """Takes a city name and returns current weather."""
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"


@tool
def explore_files(path: str = ".") -> str:
    """List files in a directory. Input: directory path (default '.')."""
    try:
        files = os.listdir(path)
        return "\n".join(files) if files else "Directory is empty."
    except Exception as e:
        return f"Error reading directory: {str(e)}"


@tool
def read_file(filepath: str) -> str:
    """Read file contents. Input: file path string."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a file. Input: filepath and content as separate args."""
    # NOTE: Pehle wale code mein JSON string pass karni padti thi kyunki
    # single input constraint tha. Ab @tool 2 proper arguments support karta hai!
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


tools = [run_command, read_url, get_weather, explore_files, read_file, write_file]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)


def chatbot(state: State):
    SYSTEM_PROMPT = """You are an elite Cursor-style AI Assistant operating in a terminal.
You have the power to explore the file system, read/write files, 
execute commands, and browse the web.
Think step by step. Use tools when needed. Be precise.

Always make sure to keep your generated codes and files in chat_gpt/ folder. You can create one if not already there 
"""
    full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages" : [llm_with_tools.invoke(full_messages)]} 


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

