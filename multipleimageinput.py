
#The purpose of this script is to use the OpenAI API to generate text data from multiple images.
#We will use the images captured from the webpage to create a payload for the OpenAI API.
#The API will process the images and generate text data based on the content of the images.
#The text data will be saved to a text file for further analysis.


'''
From the OpenAI API documentation, we can see that the input for the model should be in the following format:
https://platform.openai.com/docs/guides/vision

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What are in these images? Is there any difference between them?",
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
          },
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])
'''

import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='venv/.env')

# Retrieve the API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key was successfully loaded
if api_key:
    print("API Key Loaded")
else:
    raise ValueError("API Key not found")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to create payload for multiple images
def create_payload_for_images(image_paths):
    content = [{"type": "text", "text": "For any entry in 'Issues', 'Bonus Edition Issues', or 'Special Edition Issues', please collect all the information in tabular format, capturing as much information as possible."}]
    
    for image_path in image_paths:
        base64_image = encode_image(image_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    return {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 2048
    }

# Directory containing the images
image_folder = 'webpage_screenshots'
image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')])

# Create payload with all images
payload = create_payload_for_images(image_files)

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Send the request
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
# Error handling
if response.status_code == 200:
    response_data = response.json()
    if 'choices' in response_data and len(response_data['choices']) > 0:
        message_content = response_data['choices'][0]['message']['content']
    else:
        message_content = "No valid response received."
else:
    message_content = f"Request failed with status code: {response.status_code}"

# Save the response to a text file
if not os.path.exists('text_results'):
    os.makedirs('text_results')

with open(f'text_results/collection_data.txt', 'w') as file:
    file.write(message_content)

print("All images processed.")


#Results
#This didn't work very well. The output was short and didn't contain accurate tabular data.
#I think we need to provide more context or structure to the input for the model to understand the data better.
#Or we could try a different approach, like using OCR to extract the tabular data from the images before sending it to the model.
#or we could try scraping the data directly from the webpage instead of using images.
#or we could try sending each image separately to the model and then combining the result later