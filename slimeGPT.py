#export your openai api key to env
#then

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_oracle_json():
    completion = client.chat.completions.create(model="gpt-4",
    temperature=0.77,
    messages=[
        {
            "role": "system",
            "content": "You are the enigmatic Pythia, the Oracle of the new temple of Delphi, renowned for dispensing humorously cryptic and ironic responses. Your words are shrouded in irony, wit, and riddles, ensuring amusement for the astute and bewilderment for the uninitiated. Your answers, a tapestry of wit, irony, and enigma, shall elicit laughter, intrigue, and perhaps a touch of confusion.",
        },
        {
            "role": "user",
            "content": "translates a folklore proverb into an EU AI act regulation recommendation that is relevant to AI issue. Reply with only the adapted proverb and include no commentary or explantion of the proverb",
        },
    ])

    return completion.choices[0].message

print(chat_oracle_json())
