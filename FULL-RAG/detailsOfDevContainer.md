# Ye VS Code Dev Container setup hai. Matlab:
"Mera poora development environment Docker ke andar chalega, aur VS Code directly us container se connect ho jayega."

# Full system design
Dockerfile : Pehle ek image banai — Ubuntu base + Python + sab tools install kiya  uska andr

Phir .yaml file se 3 containers uthaye:
  - app container     → uthaya hamari local Dockerfile se bani image sa
  - mongo container   →  uthaya internet se official MongoDB image sa
  - valkey container  →  uthaya internet se official Valkey image sa

Teeno ek hi network pe hain → aapas mein baat kar sakte hain

Ab VS Code ne app container mein entry maari:
  - Tera LOCAL code folder → container ke andar MOUNT ho gaya
  - vs code Extensions + settings → devcontainer.json se auto-install ho gayi app container mai

VS Code physically tera laptop pe hi hai
  → lekin kaam container ke andar jaake karta hai (Remote Container extension)
  → isliye tujhe locally kuch bhi install nahi karna padta



# Run fastapi server:
uvicorn main:app --reload
  Breakdown:
  main → file name (main.py)
  app → FastAPI object ka naam
  --reload → auto restart (dev ke liye)

# Case : .sh file run karna
cmd: sh start.sh

👉 Ye bas shortcut hai lamba command na likhna ka 
Inside file likha hota hai:
uvicorn main:app --reload

# uvicorn main:app --host 0.0.0.0 --port 8000
main:app → tera FastAPI file + object
--port 8000 → port number
--host 0.0.0.0 → sab IPs se access allow




# Valkey : to use it we use rq package for python
The Worker:
To start executing enqueued function calls (i.e worker) in the background, start a worker from your project’s directory:

** rq worker --with-scheduler (run this on terminal to get o/p of queue worker)


# Full Flow:

POST /upload → Save PDF → MongoDB (status: "queued") → RQ Job Queue
                                                            ↓
                                                   Background Worker
                                                            ↓
                                              PDF → Image → Base64 encode
                                                            ↓
                                                 OpenAI GPT-4o Vision API
                                                            ↓
                                              Save result → MongoDB (status: "processed")
                                                            ↓
                                              GET /{id} → Return result
