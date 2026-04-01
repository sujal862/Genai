## see mini cursor - tool calling - langraph before this 
from dotenv import load_dotenv
load_dotenv()

from .graph import create_chat_graph # import it after load_env because graph.py uses OPENAI_API_KEY
from langgraph.checkpoint.mongodb import MongoDBSaver
MONGODB_URI = "mongodb://localhost:27017/"
# This is your conversation ID :-
# Same ID → same memory ; Different ID → new conversation
config = {"configurable": {"thread_id": "2"}}

# using invoke : tab tak kuch nahi milta jab tak graph pura khatam na ho, ek final state object return hota hai END mai
# using stream : har step pe event milta hai jab tak graph execute ho raha hota hai, har ek node ke execute hone ke baad uska output milta hai, aur END par bhi final state object milta hai
def init():
    # Create MongoDB checkpointer using connection string, 'with' ensures connection is opened and closed properly
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        # Create graph with memory Now your Graph remebers messages and save them in MongoDB
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)

        while True:
            user_input = input("> ")
           # state direct json mai provide kr rha hu 
            for event in graph_with_mongo.stream({ "messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"): # we are using stream_mode="values" to get the values of the state & config is used to tell graph which thread to use for memory (i.e. which conversation)
                if "messages" in event:
                    event["messages"][-1].pretty_print() # print last message

init()


# Checkpoints allow LangGraph agents to persist their state within and across multiple interactions.  (Checkpointing = Saving the graph state so it can be resumed later.)
# A checkpoint is a snapshot of the graph state at a given point in time, identified by a unique, monotonically increasing ID.

# run this file as  : python -m app.main , This runs a module as part of a package (app) and Import system works properly
# -m means: Run this as a module inside a package(app)