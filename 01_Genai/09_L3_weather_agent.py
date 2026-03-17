import json

from dotenv import load_dotenv
from openai import OpenAI
import requests
import subprocess

load_dotenv()

client = OpenAI()

# safe way to run command 
ALLOWED_COMMANDS = ["git", "dir", "ls", "echo", "cat", "type", "mkdir"]
def run_command(command):
    # We only check the main command(1st one i.e base), not its whole arguments.
    base_cmd = command.split()[0]

    if base_cmd not in ALLOWED_COMMANDS:
        return "Command not allowed."
    # run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True) # This captures and converts output into normal Python string.

    # if returncode != 0  then error output by result.stderr
    if result.returncode != 0:
        return result.stderr

    return result.stdout #returns the command output.


def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)

    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Executes any shell command on the system such as creating files, listing directories, or running programs"
    }
}

# this will give like : 
# - get_weather: Takes a city name as an input and returns the current weather for the city
# - run_command: "Executes any shell command on the system such as creating files, listing directories, or running programs"
tools_description = "\n".join(
    f"- {name}: {tool['description']}"
    for name, tool in available_tools.items()
)

# LLM is just a brain , i am providing him Hands and legs so that it can use these hand and legs to fetch the current weather 
system_prompt=f"""
    You are an helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool, and based on the tool selection you perform an action to call the tool.
    wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input.
    - Crefully analyse the user query.

    Output JSON Format:
    {{
    "step": "string", 
    "content": "string",
    "function": "The name of function if the step is action".
    "input" : "The input parameter for the function",
    }}

    Available Tools: {tools_description}
    

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step" :"plan", "content" : "The user is intrested in weather data of new york"}}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""


messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    user_query = input('> ')
    messages.append({"role":"user", "content":user_query})

    while True:
    
        response = client.chat.completions.create(
            model="gpt-5-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            # dict.get(key, default_value)
            # If key exists → return its value  If key does NOT exist → return default_value i.e False here
            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                continue


        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break

