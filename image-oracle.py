import os
from dotenv import load_dotenv
import openai

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Set the API key for the openai package
openai.api_key = API_KEY

# Define the image URL
image_url = "https://www.weizenbaum-institut.de/media/Personenbilder/fg2_kera_web.jpg"

# Define messages with system and user roles
messages = [
    {
        "role": "system",
        "content": "You are my evil mother in law."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What do you see in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                },
            },
        ],
    }
]

# Make a request to analyze the image
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=300
)

# Print the response
print(response.choices[0].message.content)
