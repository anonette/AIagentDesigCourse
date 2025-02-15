# Oracle AI

An AI-powered Oracle that generates mystical insights by combining traditional proverbs with AI regulations, complete with voice synthesis.

## Visual Studio Code Setup

1. Open the project in VS Code:
   - File -> Open Folder -> Select the project folder

2. Install recommended extensions:
   - Python (ms-python.python)
   - Python Environment Manager

3. Set up the environment:
   - Open VS Code terminal (View -> Terminal)
   - Create virtual environment:
     ```bash
     python -m venv venv
     ```
   - VS Code will detect the new environment and ask to select it as interpreter
   - Or manually select: Ctrl+Shift+P -> "Python: Select Interpreter" -> Choose ./venv/Scripts/python.exe

4. Install requirements:
   ```bash
   pip install -r requirments.txt
   ```

5. Set up API keys:
   - Create .env file in the root directory
   - Add your keys:
     ```
     OPENAI_API_KEY="your-openai-key"
     ELEVENLABS_API_KEY="your-elevenlabs-key"
     ```

6. Run the Oracle:
   - Open slimeGPT2024.py
   - Click the "Run Python File" play button in the top right
   - Or use the integrated terminal:
     ```bash
     python slimeGPT2024.py
     ```

## Quick Start (Windows)
Alternatively, simply double-click `start.bat` and it will:
1. Create a virtual environment if needed
2. Install all required packages
3. Create a template .env file if needed (you'll need to add your API keys)
4. Start the Oracle AI

## Manual Setup

### API Keys
You need to set up two API keys in a `.env` file:
- `OPENAI_API_KEY` - Get from [OpenAI](https://platform.openai.com/)
- `ELEVENLABS_API_KEY` - Get from [ElevenLabs](https://elevenlabs.io/)

### Dependencies
The project requires the following Python packages:
- `openai` - For GPT-4 integration and AI responses
- `elevenlabs` - For text-to-speech voice synthesis
- `python-dotenv` - For environment variable management
- `flask` and `flask-socketio` - For web server functionality
- `python-socketio` - For WebSocket support
- `streamlit` - For web interface

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
