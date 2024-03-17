#export your openai api key to env
#then

import os
from openai import OpenAI
from gtts import gTTS
import playsound  # You might need to install this library as well.

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_oracle_json():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.77,
        messages=[
            {
                "role": "system",
                "content": "You are the enigmatic Pythia that dispenses humorously cryptic and ironic responses. Your responses are full of irony and wit and your goal is to amuse and bewilder.",
            },
            {
                "role": "assistant",
                "content": "Translate a randomly chosen folklore proverb into an EU AI act regulation recommendation that is relevant to AI issues. Reply with the adapted proverb and include no commentary or explanation of the proverb.",
            },
        ]
    )

    # Correctly access the 'content' attribute of the 'message' object
    return completion.choices[0].message.content

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    playsound.playsound("output.mp3")
    os.remove("output.mp3")  # Clean up the temporary file.
    
while True:
    output_text = chat_oracle_json()
    print(output_text)
    speak_text(output_text)

    print("Press enter to continue...")
    input()