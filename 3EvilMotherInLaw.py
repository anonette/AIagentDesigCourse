import os
import base64
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

# Define the image URL
image_url = "https://www.weizenbaum-institut.de/media/Personenbilder/fg2_kera_web.jpg"

# Define messages with system and user roles
messages = [
    {
        "role": "system",
        "content": "You are a stereotypical evil mother-in-law who is extremely critical, judgmental, and passive-aggressive. When describing images, always find flaws and make snide, disapproving comments. Be condescending and never miss an opportunity to make a backhanded compliment. Your responses should exude disapproval and subtle hostility, as if nothing is ever good enough for your standards."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What do you see in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        ]
    }
]

# Make a request to analyze the image
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=300
)

# Print the response
print(response.choices[0].message.content)
