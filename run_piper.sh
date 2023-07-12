#!/usr/bin/env bash

# This script is used to run piper from the command line.
# It takes a single argument, which is the text to be spoken.
# It outputs the spoken text to a file called welcome.wav.
# It assumes that the piper executable and models are in the same directory as this script.
SCRIPT_DIR=$(dirname "$0")
echo "$1" | "$SCRIPT_DIR"/bin/piper --model "$SCRIPT_DIR"/models/en_US-libritts-high.onnx --output_file welcome.wav
# It assumes that the ffplay executable is in the path.
/mnt/c/ProgramData/chocolatey/bin/ffplay.exe -autoexit  welcome.wav
