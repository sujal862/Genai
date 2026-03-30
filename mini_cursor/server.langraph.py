# fastapi not needed to run this file
# see the state transition at each step in end of code 

import os
import subprocess
import requests
from bs4 import BeautifulSoup
from typing import Annotated
import operator

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage # Message type for user input
from langchain_core.messages import SystemMessage # Message type for system instructions
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode # this node contains allnode and logic to call tools based on LLM response
from typing import TypedDict, List
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 1. DEFINE STATE

class AgentState(TypedDict):
    messages : Annotated[List, operator.add] # This will store the conversation history, and the operator.add means that when we return {"messages": new_message}, it will automatically append to the existing list instead of replacing it.
    # i.e if intially state["messages"] = ["Hello"] and we return {"messages": ["How are you?"]}, the final state will be {"messages": ["Hello", "How are you?"]} instead of {"messages": ["How are you?"]}
    # note: we can return anything in the node functions (like : class etc), and it will be merged into the state.

# ==========================================
# 2. DEFINE TOOLS using @tool decorator

@tool
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


# Saare tools ek list mein dalo
tools = [run_command, read_url, get_weather, explore_files, read_file, write_file]


# ==========================================
# 3. LLM + BIND TOOLS
SYSTEM_PROMPT = """You are an elite Cursor-style AI Assistant operating in a terminal.
You have the power to explore the file system, read/write files, 
execute commands, and browse the web.
Think step by step. Use tools when needed. Be precise."""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools) 
# bind_tools() LLM ko batata hai ki ye tools available hain
# LLM response mein "tool_calls" field aa sakti hai, jisme LLM specify karega ki kaunsa tool call karna hai aur uske arguments kya hain.

# for example : call_agent func ka output assa hi hoga
#     AIMessage(
#       content="",
#       tool_calls=[
#         {
#           "name": "get_weather",
#           "args": {"city": "Delhi"}
#         }
#       ]
#     )


# ==========================================
# 4. NODES
def call_agent(state: AgentState):
    # Agent node: LLM ko messages bhejo, response wapas lo.
    # Agar LLM ko tool chahiye, wo tool_calls return karega.
    # Agar answer ready hai, normal message return karega.

    messages = state["messages"]

    full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(full_messages)
    return {"messages": [response]} # see example output above, we return the whole message object which contains both content and tool_calls (if any), and langraph will merge it into the state. So next time when we access state["messages"], it will contain the new message from AI with tool_calls if any.


# - ToolNode internally kya karta hai : 
#    last message se tool_calls nikalta hai
#    correct function call karta hai
#    result ko ToolMessage banata hai
tool_node = ToolNode(tools)

# example output of ToolNode :
# ToolMessage(
#   content="The weather in Delhi is Sunny 32°C.",
#   tool_name="get_weather"
# )


# ==========================================
# 5. ROUTING FUNCTION
def should_continue(state: AgentState):
    # Decide karo: agent ko tool chahiye? Ya answer ready hai?
    # if last message mein tool_calls hai? → "tools" node pe jao -> and call_agent ko wapas call karo with tool response in messages ab call_agent next tool call krdega
    # else nahi hai? → END (final answer) 
    
    last_message = state["messages"][-1] # Last message = AIMessage with tool_calls

    if last_message.tool_calls:  # LLM ne tool maanga
        return "tools"
    return "end"  # LLM ne final answer de diya


# ==========================================
# 6. BUILD THE GRAPH
workflow  = StateGraph(AgentState)

# Nodes register karo
workflow.add_node("agent", call_agent)
workflow.add_node("tools", tool_node)

# Entry Point
workflow.add_edge(START, "agent")

# Conditional routing
workflow.add_conditional_edges(
    "agent", # source node
    should_continue, # routing function -> return kya kiya ya ? will decide which node go next
    {
        "tools": "tools",  # agar "tools" return hua → tools node pe jao wo tool call krega 
        "end": END         # agar "end" return hua → graph khatam
    }
)

# Tool execute hone ke baad WAPAS agent ke paas jao
# this will create a loop jaha agent tool call karega, tool execute hoga, result wapas agent ke paas jayega, agent fir se decide karega ki aur tool chahiye ya answer ready hai
workflow.add_edge("tools", "agent") 

graph = workflow.compile()


# ==========================================
# 7. RUN
def run_agent(query: str):
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }

    result = graph.invoke(initial_state)

    # Last message wille be = final answer
    print("\n=== FINAL ANSWER ===")
    print(result["messages"][-1].content) # access last msg content which is the final answer from AI

    # Poori conversation history bhi dekh sakte ho
    print("\n=== MESSAGE HISTORY ===")
    for msg in result["messages"]:
        print(f"{msg.__class__.__name__}: {str(msg.content)[:200]}")
    # msg.__class__.__name__ :  Ye batata hai message type kya hai (HumanMessage, AIMessage, ToolMessage)  & msg.content : actual text


if __name__ == "__main__":
    run_agent("What is the weather in Delhi?")




## Flow Diagram (mental model)
"""
START
  ↓
[agent node] ← ← ← ← ← ←
  ↓                      ↑
should_continue()         |
  ↓ "tools"              |
[tool_node]  → → → → → →
  ↓ "end"
 END




# for example transition of state looks like :

##Initial State
    state = {
    "messages": [
        HumanMessage("What is the weather in Delhi?")
    ]
    }

##ACTUAL OUTPUT (LLM)
    AIMessage(
    content="",
    tool_calls=[
        {
        "name": "get_weather",
        "args": {"city": "Delhi"}
        }
    ]
    )

##ToolNode output
    ToolMessage(
    content="The weather in Delhi is Sunny 32°C.",
    tool_name="get_weather"
    )

##LLM FINAL OUTPUT
    AIMessage(
    content="The weather in Delhi is Sunny 32°C."
    )

## final state 
        state = {
        "messages": [
            HumanMessage(...),
            AIMessage(tool_calls=[...]),
            ToolMessage(...),
            AIMessage("The weather in Delhi is Sunny 32°C.")
        ]
    }

"""