import streamlit as st
import os
import time
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Initialize session state for debugging
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = []

def log_debug(message):
    st.session_state.debug_info.append(message)

# Display any startup debug information
st.write("Starting Sacred Symbol Oracle...")
log_debug("Application starting")

# Function to get API key
def get_api_key():
    # First try environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        log_debug("Found API key in environment variables")
        return api_key
        
    # Then try streamlit secrets
    try:
        if 'openai' in st.secrets:
            log_debug("Found API key in Streamlit secrets")
            return st.secrets['openai']['OPENAI_API_KEY']
    except Exception as e:
        log_debug(f"Error reading Streamlit secrets: {str(e)}")
    
    log_debug("No API key found")
    return None

# Display debug information
st.sidebar.markdown("### 🔧 Debug Information")
for msg in st.session_state.debug_info:
    st.sidebar.text(msg)

# Get API key
api_key = get_api_key()

if not api_key:
    st.error("""
    ⚠️ OpenAI API key not found! 
    
    Please set up your API key in one of these ways:
    1. In environment variables as OPENAI_API_KEY
    2. In `.streamlit/secrets.toml`:
       ```toml
       [openai]
       OPENAI_API_KEY = "your-key-here"
       ```
    """)
    st.stop()

try:
    client = OpenAI(api_key=api_key)
    log_debug("OpenAI client initialized successfully")
except Exception as e:
    st.error(f"Error initializing OpenAI client: {str(e)}")
    log_debug(f"OpenAI client error: {str(e)}")
    st.stop()

# Debug information
st.write("Debug Info:")
st.write(f"Current file: {__file__}")
st.write(f"Streamlit version: {st.__version__}")

# Set page title and description
st.title("✨ Sacred Symbol Oracle")
st.markdown("""
This oracle will generate a unique sacred symbol based on your name.
The symbol contains hidden elements that hint at a personal cosmic message.
""")

def generate_sacred_symbol(name):
    """Generate a sacred symbol based on the user's name."""
    with st.status("🔮 Generating your sacred symbol...", expanded=True) as status:
        # Create a detailed prompt for the image generation
        prompt = f"""Generate a unique, sacred symbol that represents a personal cosmic message for {name}. 
        The glyph should resemble ancient runes, celestial diagrams, or alchemical sigils.
        It should include hidden elements that hint at an interpretation, with layered, intersecting lines and geometric symmetry.
        The symbol should be mystical, intricate, and personalized to the essence of the name {name}.
        Use a dark background with luminous, glowing lines in gold, silver, or ethereal blue.
        The symbol should appear as if it was discovered in an ancient grimoire or celestial map."""
        
        try:
            status.write("Channeling cosmic energies...")
            
            # Generate the image using DALL-E
            response = client.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            # Get the image URL
            image_url = response.data[0].url
            
            status.write("Manifesting symbol...")
            
            # Download the image
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            
            # Create output directory if it doesn't exist
            os.makedirs("oracle_symbols", exist_ok=True)
            
            # Save the image with a timestamp to avoid overwriting
            timestamp = int(time.time())
            image_path = f"oracle_symbols/{name}_sacred_symbol_{timestamp}.png"
            image.save(image_path)
            
            status.write("Symbol has been manifested!")
            status.update(label="✨ Sacred symbol generated!", state="complete")
            
            return image, image_path
            
        except Exception as e:
            st.error(f"Error generating sacred symbol: {e}")
            return None, None

# Create input form
with st.form("oracle_form"):
    name = st.text_input("Enter your name:", placeholder="Your name here...")
    generate_button = st.form_submit_button("Generate Sacred Symbol")

# Generate symbol when form is submitted
if generate_button and name:
    image, image_path = generate_sacred_symbol(name)
    
    if image and image_path:
        # Display the image
        st.image(image, caption=f"Sacred Symbol for {name}", use_column_width=True)
        
        # Display interpretation
        st.markdown("### 🌟 Interpretation of Your Sacred Symbol")
        st.markdown(f"""
        This unique cosmic glyph contains elements that resonate with **{name}'s** spiritual essence.
        
        - The intersecting lines represent the convergence of past, present, and future paths
        - Hidden within its geometry are symbols of personal strength and cosmic connection
        - The luminous patterns reflect your inner light and potential
        - Each angle and curve holds meaning specific to your journey
        
        _Meditate on this symbol to reveal deeper meanings unique to your path._
        """)
        
        # Add download button
        with open(image_path, "rb") as file:
            btn = st.download_button(
                label="Download Your Sacred Symbol",
                data=file,
                file_name=os.path.basename(image_path),
                mime="image/png"
            )
            
# Add session history
if "generated_symbols" not in st.session_state:
    st.session_state.generated_symbols = []

# Display previous generations in a sidebar
with st.sidebar:
    st.markdown("### 📜 Previous Symbols")
    if len(st.session_state.generated_symbols) > 0:
        for prev_name in st.session_state.generated_symbols:
            st.markdown(f"- {prev_name}")
    else:
        st.markdown("_No symbols generated yet in this session_")

# Footer
st.markdown("---")
st.markdown("_🔮 Created with mystical algorithms and cosmic wisdom_")
