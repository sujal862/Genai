# Microsoft ka ready-made light image use kar raha hai
# Isme pehle se hai installed: Ubuntu + Python 3.12 + common dev tools
FROM mcr.microsoft.com/devcontainers/python:3.12 

# Python ka output buffered nahi hoga
# Matlab print() ka output seedha terminal mein dikhega — real time
# Bina is ke logs delay se aate hain
ENV PYTHONUNBUFFERED=1

# apt-get = Ubuntu ka package manager (npm jaisa, but OS level)
# update = available packages ki list refresh karo
# curl = URLs se data fetch karne ka tool (APIs test karne, files download karne)
RUN sudo apt-get update && \
    sudo apt-get install -y curl

# for pdf2image
RUN apt-get install -y poppler-utils

# pip ko latest version pe upgrade karo
# Taki koi bhi package install karte waqt version issues na aayein
RUN pip install --upgrade pip