# Sacred Symbol Oracle

A mystical web application that generates unique sacred symbols based on your name using OpenAI's DALL-E.

## Features

- Beautiful Streamlit interface
- Secure API key handling
- Image generation with DALL-E
- Download generated symbols
- Detailed interpretations

## Local Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application locally:
   ```bash
   streamlit run imageoutput-oracle.py
   ```

## Online Deployment

### Deploying to Streamlit Cloud

1. Create a free account at [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. In the Streamlit Cloud dashboard:
   - Go to "Settings" > "Secrets"
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
4. Deploy the app

### Deploying to other platforms

For other platforms like Heroku or Railway, you'll need to:
1. Set up the environment variable `OPENAI_API_KEY` in your platform's configuration
2. Follow the platform-specific deployment instructions
3. Make sure to include all dependencies from `requirements.txt`

## Security Notes

- Never commit your `.env` file or expose your API key
- The application uses secure input fields for API key entry
- API keys are stored in environment variables

## License

MIT License
