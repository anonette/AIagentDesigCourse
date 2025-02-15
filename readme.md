# Oracle AI

An AI-powered Oracle that generates mystical insights by combining traditional proverbs with AI regulations, complete with voice synthesis.

## Requirements

### API Keys
You need to set up two API keys in a `.env` file:
- `OPENAI_API_KEY` - Get from [OpenAI](https://platform.openai.com/)
- `ELEVENLABS_API_KEY` - Get from [ElevenLabs](https://elevenlabs.io/)

### Python Environment
1. Python 3.x
2. Virtual Environment (venv)

### Dependencies
The project requires the following Python packages:
- `openai` - For GPT-4 integration and AI responses
- `elevenlabs` - For text-to-speech voice synthesis
- `python-dotenv` - For environment variable management
- `flask` and `flask-socketio` - For web server functionality
- `python-socketio` - For WebSocket support
- `streamlit` - For web interface

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

2. Install requirements:
```bash
pip install -r requirments.txt
```

3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY="your-openai-key"
ELEVENLABS_API_KEY="your-elevenlabs-key"
```

## Usage

### Core Oracle AI
Run the main Oracle AI script:
```bash
python slimeGPT2024.py
```
- Press Enter to generate each new Oracle response
- Each response includes a proverb and an AI regulation
- Responses are both displayed and spoken aloud

### Web Interface
Run the Streamlit web interface:
```bash
streamlit run streamlit_app2.py
```
- Upload log files for processing
- Process messages with different voice options
- Listen to audio playback in the browser
