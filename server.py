import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import subprocess
import datetime
import csv

from flask import Flask, request, after_this_request



app = Flask(__name__)

def chat_oracle():
    try:
        completion = client.chat.completions.create(model="gpt-4",
            temperature=0.77,
            messages=[
                {
                    "role": "system",
                    "content": "You are Pythia from the new temple of Delphi. Known to be ironic and funny. Your answers short and a bit cryptic to the layman.",
                },
                {
                    "role": "user",
                    "content": "translates a folklore proverb into an EU AI act regulation recommendation that is relevant to AI issue. Reply with only the adapted proverb and include no commentary or explanation of the proverb",
                },
            ])

        # Access the message content using the correct attribute
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@app.route('/tts', methods=['POST'])
def text_to_speech():
    oracle_output = chat_oracle()

    # Generate a timestamped filename for the output audio file
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = "tts-output/tts_{}.wav".format(timestamp)

    # Generate the command to convert text to speech
    piper_cmd = ["./bin/piper", "--model", "./models/en_US-libritts-high.onnx", "--output_file", output_file]
    piper = subprocess.Popen(piper_cmd, stdin=subprocess.PIPE)
    piper.communicate(oracle_output.encode())

    @after_this_request
    def play_audio(response):
        if piper.returncode == 0:
            # Play the audio file
            subprocess.run(["/mnt/c/ProgramData/chocolatey/bin/ffplay.exe","-af", "adelay=3s:all=1", "-autoexit", output_file], check=True)
            
            # Save results to CSV file
            with open('results.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([oracle_output, output_file])
        return response

    return oracle_output, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
