## copied from main.py
from dotenv import load_dotenv
import json
load_dotenv()

from .graph import create_chat_graph 
from langgraph.types import Command
from langgraph.checkpoint.mongodb import MongoDBSaver
MONGODB_URI = "mongodb://localhost:27017/"
config = {"configurable": {"thread_id": "2"}}

def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)

        state = graph_with_mongo.get_state(config) # get the state of the graph
        for message in state.values["messages"]:
            message.pretty_print()

        # last_message = state.values["messages"][-1]
        # # Access tool_calls attribute directly (it's a list)
        # tool_calls = getattr(last_message, "tool_calls", [])

        # user_query = next((call['args'].get('query') for call in tool_calls  # list comprehension to find query 
        #                 if call['name'] == 'human_assistance_tool'), None)

        # print(f"User is Trying to Ask: {user_query}")
        # if user_query:
        #     ans = input("Resolution > ")

        # # resume the graph after human provides the response 
        # # command : is used to resume the graph, and we provide resume=data to the interrupt tool
        # resume_command = Command(resume = {"data": ans})
        # for event in graph_with_mongo.stream(resume_command, config, stream_mode="values"):
        #     if "messages" in event:
        #         event["messages"][-1].pretty_print()

init()

