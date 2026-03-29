from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

# Schema define (AI response ka structure fix karne ke liye)
class DetectCallResponse(BaseModel):
    is_coding_question: bool

class CodingAIResponse(BaseModel):
    answer: str

client = wrap_openai(OpenAI()) # for langsmith tracing and debugging

# State = shared memory (har node isko read/update karega)
class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool

# 🔹 State = shared memory (har node isko read/update karega)
def detect_query(state: State):
    user_message = state['user_message']

    SYSTEM_PROMPT = """
    You are an AI assistant . Your job is to detect if the user's query is related 
    to coding question or not.
    Return the response in specified JSON boolean only"""

    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=DetectCallResponse, # use the pydantic model to parse the response
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    state["is_coding_question"] = result.choices[0].message.parsed.is_coding_question
    return state

# 🔹 Conditional function: decide next node
def route_edge(state: State) -> Literal["solve_coding_question", "solve_simple_question"]:
    if state["is_coding_question"]:
        return "solve_coding_question"
    else:
        return "solve_simple_question"
    

def solve_coding_question(state: State):
    #openaai call to solve coding question
    user_message = state['user_message']
    SYSTEM_PROMPT = """
    You are an expert programmer AI assistant . Your job is to solve the user's coding question and provide the solution.
    """

    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=CodingAIResponse, # use the pydantic model to parse the response
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state

def solve_simple_question(state: State):
    #openaai call to solve simple question
    user_message = state.get("user_message")

    # OpenAI Call (Coding Question gpt-mini)
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to chat with user
    """

    # OpenAI Call
    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=CodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        ]
    )
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state


# Graph build start
graph_builder = StateGraph(State)

#  Nodes add (tasks define kar rahe hain)
graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)

# entry point  = start node
graph_builder.add_edge(START, "detect_query")
graph_builder.add_conditional_edges(
    "detect_query", # Ye source node hai (yaha se decision start hoga)
    route_edge # Ye function state ko check karega , aur decide karega next kaunsa node run hoga
    )

# 🔹 Start → first node
graph_builder.add_edge("solve_coding_question", END)
graph_builder.add_edge("solve_simple_question", END)


graph = graph_builder.compile()

def call_graph(user_message: str):
    state = {
        "user_message": user_message,
        "ai_message": "",
        "is_coding_question": False
    }
    result = graph.invoke(state)

    print("final result:", result)

call_graph("How to write cpp code to add 2 numbers ?")