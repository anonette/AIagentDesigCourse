# Suppress pydantic warnings at the very start
import warnings
warnings.filterwarnings("ignore")

import os
import openai
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

client = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"), # Defaults to ELEVEN_API_KEY
)
def chat_oracle_json():
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            temperature=0.8,
            messages=[
                {
                    "role": "system",
                    "content": "You are the Oracle of Delphi, a mystical figure known for delivering profound yet humorous and surprising insights. You draw upon obscure proverbs from global folklore to craft ironic and provocative AI regulations. Each response should reflect wisdom, wit, and irony, evoking both laughter and deep thought. Avoid explanation or elaboration and let the proverbs and regulations speak for themselves",
                },
                {
                    "role": "user",
                    "content": "In your response, first cite the original proverb, then follow with an adapted AI regulation inspired by it. The regulation should spark wonder, amusement, and irony, with no additional commentary or clarification. Keep it always one proverb and adaptation per response.",
                },
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"Error generating chat completion: {e}")
        return None

def generate_audio_from_text(text, voice_id='Rachel'):
    try:
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        play(audio)
    except Exception as e:
        print(f"Error generating audio: {e}")

print("\n=== Oracle AI is ready to share wisdom ===\n")
while True:
    output_text = chat_oracle_json()
    if output_text:
        print(output_text + "\n")
        generate_audio_from_text(output_text, voice_id='Rachel')
    
    input("Press Enter for next Oracle response...")
