from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model 
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.types import interrupt
from langgraph.prebuilt import ToolNode, tools_condition

# Ai -> call this tool with the query -> state got saved in DB and graph exection exit out -> Human -> provide response -> Now the graph gets the whole state + human response and graph resumes
@tool()
def human_assistance_tool(query: str): 
    """Request assistance from a human""" # this is the discription of this tool what it does
    human_response = interrupt({'query': query}) # it will pause the execution of graph after saving data states in DB and wait for the human response
    return human_response["data"] # it will return the data from the human response and resume the execution of graph

tools=[human_assistance_tool]

# llm internally calls the openai api and gets the response
llm = init_chat_model(model_provider="openai", model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

# (LLM call) : it takes in the current state and returns the new state after processing the messages with the LLM
def chatbot(state: State):
    return {"messages" : [llm_with_tools.invoke(state["messages"])]} # LLM call happening, response will contain either normal chat answer or tool_calls

tool_node = ToolNode(tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition, # if the LLM requests a tool call then go to tool_node else go to END
)

graph_builder.add_edge("tools", "chatbot")

# graph without any memory (not using this now!)
graph = graph_builder.compile()

# this will create a new graph with checkpointer (to store states)
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)



# Note :
# When you use tools_condition on a node, Langgraph implicitly creates the routing to either your "tools" node or the END node depending on whether the LLM requested a tool execution.

# START → chatbot
#             ↓
#      tools_condition
#        ↙        ↘
#    tools        END
#      ↓
#   chatbot