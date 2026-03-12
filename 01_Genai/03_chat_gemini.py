from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyBhTEaiyu2Lp6KfaY96vM17_Puyg0KiIwo')

response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Why is the sky blue?'
)
print(response.text)