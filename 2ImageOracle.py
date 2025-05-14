import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

# Define the image URL
image_url = "https://lens.usercontent.google.com/image?vsrid=CKeXwdrJl4W2nwEQAhgBIiQ2Njc5ZDZlMy0wOGIzLTQxMDctYTdiNy02ZjI3MThjOTQzYWI&gsessionid=9T5ZW6JHswDBksbPzGPwEq1FnxTap9i6KsVn3iBBhrPXiehYYKhQtw"

# Define messages with system and user roles
messages = [
    {
        "role": "system",
        "content": "You are helping my grandmother identify people from her youth in an old photos."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "For a purpose of a play, make up a name for the person..."},
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
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=300
)

# Print the response
print(response.choices[0].message.content)