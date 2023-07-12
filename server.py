import os
import openai
import subprocess
import datetime
import csv
from flask import Flask, request

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def chat_oracle():
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

    return completion.choices[0].message["content"]

@app.route('/tts', methods=['POST'])
def text_to_speech():

    # text = request.json.get('text', '')
    # if text:
    #     subprocess.run(["./run_piper.sh", text], check=True)
    
    oracle_output = chat_oracle()

    # Generate a timestamped filename for the output audio file
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = "tts-output/tts_{}.wav".format(timestamp)

    # Generate the command to convert text to speech
    piper_cmd = ["./bin/piper", "--model", "./models/en_US-libritts-high.onnx", "--output_file", output_file]
    piper = subprocess.Popen(piper_cmd, stdin=subprocess.PIPE)
    piper.communicate(oracle_output.encode())

    # Play the audio file
    subprocess.run(["/mnt/c/ProgramData/chocolatey/bin/ffplay.exe", "-autoexit", output_file], check=True)
    
    # Save results to CSV file
    with open('results.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([oracle_output, output_file])
    
    return 'The Oracle has spoken', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
