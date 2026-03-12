import json
from collections import Counter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
# Self-Consistency Prompting: The model generates multiple responses and selects the most consistent or common answer.

question = "What is greator ? 9.8 or 9.11 ; context may vary may be its in numerical or may be books page numbers"

NUM_SAMPLES = 5
answers = []

for i in range(NUM_SAMPLES):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a math reasoning assistant. Solve step by step and return the probable answer according to context as JSON {answer: string}"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.7   # randomness for different reasoning paths
    )

    result = json.loads(response.choices[0].message.content)

    answers.append(result["answer"])

    print(f"Run {i+1}: {result['answer']}")

# majority voting
most_common_answer = Counter(answers).most_common(1)[0][0]

print("\nFinal Answer (Self Consistency):", most_common_answer)