


from openai import OpenAI

import re
import httpx
import os
from dotenv import load_dotenv
import json
import base64
import requests


_ = load_dotenv(dotenv_path='venv/.env')

# Retrieve the API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key was successfully loaded
if api_key:
    print("API Key Loaded")
else:
    print("API Key not found")


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
image_path = "webpage_screenshot.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Summarize this image"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())

