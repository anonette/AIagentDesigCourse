#export your openai api key to env
#then

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_oracle_json():
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.77,
        messages=[
            {
                "role": "system",
                "content": "You are Pythia from the new temple of Delphi. known to be ironic and funny. your answers short and a bit cryptic to the layman.",
            },
            {
                "role": "user",
                "content": "translates a folklore proverb into an EU AI act regulation recommendation that is relevant to AI issue. Reply with only the adapted proverb and include no commentary or explantion of the proverb",
            },
        ],
    )

    return completion.choices[0].message

print(chat_oracle_json())
