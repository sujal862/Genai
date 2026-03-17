from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

result = client.chat.completions.create(
    model="gpt-4o-mini",
    # Zero-shot Prompting: The model is given a direct question or task without prior examples.
    messages=[
        {"role": "user", "content": "What is 2 + 2"} 
    ]
)

print(result.choices[0].message.content)



# choices → list of generated outputs
# [0] → first output
# message → assistant message
# content → actual generated text