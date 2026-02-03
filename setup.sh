#!/bin/bash
echo "🚀 Initializing Ainix Hosting Setup..."
sudo apt update
sudo apt install python3-tk -y
pip install flask customtkinter
sudo npm install -g localtunnel
echo "✅ Setup Complete! Run 'python3 main.py' to start."
