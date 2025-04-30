import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Set page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="Sacred Symbol Oracle",
    page_icon="🔮",
    layout="centered"
)

# Try to load from .env file, but don't fail if it doesn't exist
try:
    load_dotenv()
except Exception as e:
    pass  # Silently continue if .env file doesn't exist

# Get API key from environment or Streamlit secrets
env_key = os.getenv("OPENAI_API_KEY")
secrets_key = None

# Try to get from Streamlit secrets
try:
    secrets_key = st.secrets["OPENAI_API_KEY"]
except Exception as e:
    pass  # Silently continue if secrets don't exist

# Initialize the OpenAI client with API key from environment or Streamlit secrets
API_KEY = env_key or secrets_key

if not API_KEY:
    st.error("""
    OpenAI API key not found. Please ensure:
    1. For local development: Create a .env file with OPENAI_API_KEY=your_key
    2. For deployment: Add the key in Streamlit Cloud Secrets as OPENAI_API_KEY=your_key
    """)
    st.stop()

# Validate API key format
if not API_KEY.startswith("sk-"):
    st.error("Invalid API key format. API keys should start with 'sk-'")
    st.stop()

try:
    # Initialize the OpenAI client with explicit configuration
    client = OpenAI(
        api_key=API_KEY,
        timeout=30.0,  # 30 second timeout
        max_retries=3  # Retry failed requests up to 3 times
    )
    
    # Test the client with a simple request
    client.models.list()
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {str(e)}")
    st.stop()

def generate_sacred_symbol(name):
    """Generate a sacred symbol based on the user's name."""
    # Create a detailed prompt for the image generation
    prompt = f"""Generate a unique, sacred symbol that represents a personal cosmic message for {name}. 
    The glyph should resemble ancient runes, celestial diagrams, or alchemical sigils.
    It should include hidden elements that hint at an interpretation, with layered, intersecting lines and geometric symmetry.
    The symbol should be mystical, intricate, and personalized to the essence of the name {name}.
    Use a dark background with luminous, glowing lines in gold, silver, or ethereal blue.
    The symbol should appear as if it was discovered in an ancient grimoire or celestial map."""
    
    try:
        # Generate the image using DALL-E
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        # Create output directory if it doesn't exist
        os.makedirs("oracle_symbols", exist_ok=True)
        
        # Save the image with a timestamp to avoid overwriting
        timestamp = int(time.time())
        image_path = f"oracle_symbols/{name}_sacred_symbol_{timestamp}.png"
        image.save(image_path)
        
        return image, image_path
    
    except Exception as e:
        st.error(f"Error generating sacred symbol: {e}")
        return None, None

def main():
    st.title("🔮 Sacred Symbol Oracle")
    st.markdown("""
    Welcome to the Sacred Symbol Oracle! This mystical tool will generate a unique sacred symbol 
    based on your name, containing hidden elements that hint at a personal cosmic message.
    """)
    
    # Sidebar for API key input
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", value=API_KEY or "")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            client.api_key = api_key
    
    # Main content
    name = st.text_input("Enter your name:", placeholder="Your name here...")
    
    if st.button("Generate Sacred Symbol"):
        if not name:
            st.warning("Please enter your name first!")
        elif not client.api_key:
            st.error("Please enter your OpenAI API key in the sidebar!")
        else:
            with st.spinner("Generating your sacred symbol... This may take a moment."):
                image, image_path = generate_sacred_symbol(name)
                
                if image:
                    st.image(image, caption=f"Sacred Symbol for {name}", use_column_width=True)
                    
                    # Interpretation
                    st.markdown(f"""
                    ### Interpretation of {name}'s Sacred Symbol:
                    
                    This unique cosmic glyph contains elements that resonate with {name}'s spiritual essence.
                    The intersecting lines represent the convergence of past, present, and future paths.
                    Hidden within its geometry are symbols of personal strength and cosmic connection.
                    Meditate on this symbol to reveal deeper meanings unique to your journey.
                    """)
                    
                    # Download button
                    with open(image_path, "rb") as file:
                        st.download_button(
                            label="Download Symbol",
                            data=file,
                            file_name=f"{name}_sacred_symbol.png",
                            mime="image/png"
                        )

if __name__ == "__main__":
    main()
