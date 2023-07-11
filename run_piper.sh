#!/usr/bin/env bash
SCRIPT_DIR=$(dirname "$0")
echo "$1" | "$SCRIPT_DIR"/bin/piper --model "$SCRIPT_DIR"/models/en_US-libritts-high.onnx --output_file welcome.wav
/mnt/c/ProgramData/chocolatey/bin/ffplay.exe -autoexit  welcome.wav
