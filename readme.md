# SlimeGPT: Educational Oracle AI Agent Design Lab

A step-by-step educational project for learning and experimenting with AI agent design patterns using OpenAI's APIs. This repository demonstrates the progressive development of AI agents, starting with simple text completions and gradually integrating images, audio, and different interaction models - all with the fun use case of creating mystical and humorous oracle experiences.

## 🎓 Educational Purpose

This project serves as a practical guide for:

- Following a progression from simple to complex AI agent design
- Starting with basic text completion and gradually adding images and audio
- Learning to build fun, creative applications (oracles, fortune tellers, etc.)
- Exploring different interaction patterns (CLI, web interface, voice)
- Building multimodal AI applications that combine text, image, and audio
- Understanding how to chain AI capabilities together into cohesive experiences

## 🤖 Project Components (Progressive Learning Path)

### Level 1: Text-Only Agents
- **Oracle Text** (`1OracleText.py`): The simplest starting point - provides text-based oracle readings using GPT
- **Evil Mother-In-Law** (`3EvilMotherInLaw.py`): A character-based conversational oracle with personality

### Level 2: Adding Images to Agents
- **Image Oracle** (`2ImageOracle.py`): Introduces basic image generation based on textual descriptions
- **Image Output Oracle** (`4ImageOutputOracle.py`): Enhances the image generation with better output handling
- **Sacred Symbol Oracle** (`5imageoutput-oracle.py`): Generates personalized mystical symbols based on user names

### Level 3: Complex Multimodal Agents
- **Image Telephone Game** (`6image-telephone.py`): Implements a creative chain where images and descriptions evolve in sequence
- **Past Lives Oracle** (`7pastlives.py`, `7pastlivespeechtospeech.py`): Creates stories and images about users' past lives with added audio

### Level 4: Interactive Web Interfaces
- **Streamlit Chat** (`8streamlit_chat.py`): A web-based chat interface for conversational AI
- **Streamlit Oracle** (`9streamlit_oracle.py`): A polished web application for the Sacred Symbol Oracle

## 🛠️ Technical Skills Demonstrated

- **Progressive API Integration**: Starting with basic GPT completions and adding DALL-E and TTS APIs
- **Prompt Engineering**: Crafting effective and entertaining prompts for oracle predictions
- **Multi-modal Systems**: Learning to combine text, image, and audio generation
- **User Interface Design**: Evolving from CLI to web-based interfaces with Streamlit
- **Agent Chaining**: Building more complex applications by connecting multiple AI capabilities
- **Error Handling**: Graceful management of API limits and failures
- **File Management**: Organizing and saving generated oracle content

## 🚀 Getting Started (Complete Beginner's Guide)

### Prerequisites

#### 1. Install Python
- Download Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify installation by opening a command prompt/terminal and typing:
  ```bash
  python --version
  ```

#### 2. Install Visual Studio Code
- Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
- Install recommended extensions:
  - Python extension (by Microsoft)
  - Jupyter (for notebook files)
  - GitLens (for better Git integration)

#### 3. Set Up Git
- Download and install Git from [git-scm.com](https://git-scm.com/downloads)
- Configure Git with your name and email:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

#### 4. Get an OpenAI API Key
- Create an account at [OpenAI](https://platform.openai.com/signup)
- Navigate to [API Keys](https://platform.openai.com/api-keys)
- Create a new secret key and save it securely

#### 5. Understanding .gitignore (Important for Beginners)
- The `.gitignore` file tells Git which files to ignore when tracking changes
- This is crucial for:
  - **Security**: Preventing sensitive data (API keys, credentials) from being shared
  - **Cleanliness**: Avoiding adding generated files, cache, or logs to your repository
  - **Performance**: Keeping your repository size small and clone/pull operations fast
- Our project already includes a `.gitignore` file configured for AI development
- You should review it to understand which files are excluded from version control
- Never edit the `.gitignore` to track sensitive files like `.env` or API keys!

### Installation

1. Clone this repository
   ```bash
   # Open a terminal/command prompt
   git clone https://github.com/yourusername/slimeGPT.git
   cd slimeGPT
   ```
   
   Alternatively, if you don't use Git yet:
   - Download the ZIP from the GitHub repository
   - Extract it to a folder
   - Open a terminal/command prompt and navigate to that folder

2. Open the project in VS Code
   ```bash
   code .
   ```

3. Create and activate a virtual environment
   ```bash
   # Create the virtual environment
   python -m venv openai-env
   
   # Activate it on Windows
   openai-env\Scripts\activate
   
   # Activate it on macOS/Linux
   source openai-env/bin/activate
   ```
   
   You'll know it's activated when you see `(openai-env)` at the beginning of your terminal prompt.

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your API key using one of these methods:

   **Method A: Using a .env file (recommended for development)**
   
   Create a file named `.env` in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   
   **Method B: Using Streamlit secrets (for Streamlit apps)**
   
   Create a folder `.streamlit` and a file `secrets.toml` inside it:
   ```toml
   [openai]
   OPENAI_API_KEY = "your_api_key_here"
   ```
   
   **Method C: Set as environment variable (system-wide)**
   
   On Windows (Command Prompt):
   ```
   setx OPENAI_API_KEY "your_api_key_here"
   ```
   
   On macOS/Linux:
   ```
   echo 'export OPENAI_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Running the Examples (Follow the Learning Path)

Each Python file in the project is a standalone application that demonstrates a progressive step in AI agent design:

```bash
# Start with basic text oracle
python 1OracleText.py

# Move to image generation
python 2ImageOracle.py
python 5imageoutput-oracle.py

# Try the more complex multimodal applications
python 6image-telephone.py
python 7pastlives.py

# Explore the web interfaces last
streamlit run 8streamlit_chat.py
streamlit run 9streamlit_oracle.py
```

For the best learning experience, follow the numbered sequence of examples to see how capabilities are progressively added.

### 📋 Step-by-Step Workflow (Day-to-Day Development)

Here's the typical workflow you'll follow each time you work on this project:

#### Step 1: Open VS Code in Your Project Directory
```bash
# Navigate to your project directory
cd path/to/slimeGPT

# Open VS Code in this directory
code .
```

#### Step 2: Open a Terminal in VS Code
- In VS Code, press `` Ctrl+` `` (backtick) to open a new terminal
- Or go to Terminal → New Terminal in the menu

#### Step 3: Activate Your Virtual Environment
```bash
# On Windows
openai-env\Scripts\activate

# On macOS/Linux
source openai-env/bin/activate
```
You'll see `(openai-env)` appear at the beginning of your terminal prompt when it's activated.

#### Step 4: Run a Python Script
To run a basic Python script:
```bash
python 1OracleText.py
```

To run a Streamlit app:
```bash
streamlit run 9streamlit_oracle.py
```

#### Step 5: Stopping Applications
- For regular Python scripts, the program will stop when finished
- For Streamlit apps:
  - The app runs in your browser at http://localhost:8501 by default
  - To stop the server, go back to your terminal and press `Ctrl+C`

#### Step 6: Deactivate the Virtual Environment
When you're done working:
```bash
deactivate
```
The `(openai-env)` prefix will disappear from your terminal prompt.

## 🤖 Using AI Agents for Programming

This project not only showcases AI agents as oracles but can also be developed with the help of AI programming assistants. Here's how to leverage AI agents for your development workflow:

### Installing GitHub Copilot

GitHub Copilot is an AI pair programmer that can help you write code faster and with fewer errors. Here's how to set it up:

1. **Sign up for GitHub Copilot**:
   - Visit [GitHub Copilot](https://github.com/features/copilot) and sign up for the service
   - GitHub Copilot is free for verified students, teachers, and maintainers of popular open-source projects
   - For others, a subscription is required

2. **Install the GitHub Copilot extension in VS Code**:
   - Open VS Code
   - Go to the Extensions view by clicking the Extensions icon in the Activity Bar or pressing `Ctrl+Shift+X`
   - Search for "GitHub Copilot"
   - Click Install

3. **Authenticate GitHub Copilot**:
   - After installation, you'll be prompted to sign in to GitHub
   - Follow the authentication steps to connect your GitHub account
   - Once authenticated, Copilot will be activated in your editor

### Using GitHub Copilot for AI Agent Development

Copilot can significantly accelerate your development of AI agents in this project:

1. **Code Completion**: As you type, Copilot will suggest code completions based on context:
   - OpenAI API calls
   - Prompt templates
   - Error handling patterns
   - UI components for Streamlit

2. **Learning from Examples**: Ask Copilot to explain the existing code:
   ```python
   # Asking Copilot: Explain how this code generates oracle predictions
   ```

3. **Extending Functionality**: When adding new features to an agent:
   ```python
   # Copilot, help me add audio output to this oracle
   ```

4. **Debugging**: When you encounter errors in your agents:
   ```python
   # Copilot, debug this OpenAI API error
   ```

### Best Practices for AI-Assisted Programming

When using AI tools like GitHub Copilot for developing AI agents:

1. **Review All Suggestions**: Always review AI-generated code for:
   - Correct API usage (parameters, endpoints)
   - Security best practices (proper key handling)
   - Performance considerations
   - Alignment with your project's style

2. **Use Comments for Guidance**: Write descriptive comments to guide the AI:
   ```python
   # Generate a function that takes a user name and returns a personalized oracle reading
   # using GPT-4 with appropriate error handling
   ```

3. **Iterative Refinement**: Use AI tools to:
   - Generate a basic implementation
   - Review and edit the code
   - Ask for specific improvements
   - Refine until the code meets your requirements

4. **Learn, Don't Just Copy**: Use AI-generated code as a learning opportunity:
   - Understand why certain approaches were suggested
   - Research unfamiliar patterns or functions
   - Refactor code to improve your understanding

By combining your creativity with AI programming assistants, you can build more sophisticated and reliable AI agents while accelerating your learning process.

## 📚 Learning Resources

If you're using this project to learn about AI agent design, here are some concepts to explore:

1. **Prompt Engineering for Creativity**: Study how the prompts in each oracle create entertaining and mystical outputs
2. **Progressive Complexity**: Notice how each numbered example adds new capabilities to the previous one
3. **Chain-of-Thought**: Look at how the telephone game chains multiple AI capabilities for creative results
4. **Multimodal Integration**: Examine how text, image, and audio work together in the past lives oracle
5. **UI/UX for Oracle Applications**: Compare the CLI vs. Streamlit interfaces for mystical experiences
6. **Character Development**: Learn how to create AI agents with distinct personalities like the Evil Mother-In-Law

## 🔐 Security Notes

- Never commit your `.env` file or expose your API key
- The application uses secure handling for API keys
- API keys are stored in environment variables for security

## 📂 Project Structure Notes

- Empty folders in the repository are maintained with `.gitkeep` files
  - These are just empty placeholder files that allow git to track otherwise empty folders
  - Git doesn't track empty directories by default, but our project needs these folders to save generated content
  - You'll find these in `oracle_symbols/`, `output_audio/`, and `telephone_game/` folders
- The `.gitignore` file is configured to:
  - Exclude your API keys and environment files for security
  - Ignore generated content (images, audio) to keep the repository size small
  - Exclude Python cache files and virtual environment directories

## 📄 License

MIT License
