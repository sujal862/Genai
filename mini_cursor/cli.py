import requests

API_URL = "http://127.0.0.1:8000/chat"

print("==================================================")
print(" 🤖 AI AGENT TERMINAL INITIALIZED (Cursor Style) 🤖")
print("==================================================")
print("Type 'exit' to quit.\n")

while True:
    try:
        query = input("You > ")
        if query.lower() in ["exit", "q"]:
            print("Goodbye!")
            break
            
        print("⏳ Agent is thinking...")
        
        # Send query to our FastAPI Brain
        res = requests.post(API_URL, json={"query": query})
        data = res.json()
        
        print("\n--- Agent Activity ---")
        # Go through the array of thoughts/actions FastAPI returned
        for log in data.get("logs", []):
            print(log)
        print("----------------------\n")
            
        # Print Final Answer from the LLM
        print(f"🤖 Output: {data.get('final_answer')}\n")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect. Is your FastAPI server (uvicorn) running?\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
