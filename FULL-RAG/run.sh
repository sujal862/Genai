#!/bin/bash

# path:fastapi instance
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload

# this code is only for running server in dev enviroment nopt for production