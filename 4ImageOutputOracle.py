import os
import time
from dotenv import load_dotenv
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

def get_user_name():
    """Get the user's name from input."""
    name = input("Please enter your name: ")
    return name

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
        
        print(f"Sacred symbol for {name} has been generated and saved to {image_path}")
        
        # Provide a brief interpretation
        print(f"\nInterpretation of {name}'s Sacred Symbol:")
        print(f"This unique cosmic glyph contains elements that resonate with {name}'s spiritual essence.")
        print("The intersecting lines represent the convergence of past, present, and future paths.")
        print("Hidden within its geometry are symbols of personal strength and cosmic connection.")
        print("Meditate on this symbol to reveal deeper meanings unique to your journey.")
        
        # Display the image if in an environment that supports it
        try:
            image.show()
        except Exception as e:
            print(f"Note: Could not display the image automatically. Please open {image_path} to view it.")
        
        return image_path
    
    except Exception as e:
        print(f"Error generating sacred symbol: {e}")
        return None

def main():
    """Main function to run the oracle."""
    print("=== Sacred Symbol Oracle ===")
    print("This oracle will generate a unique sacred symbol based on your name.")
    print("The symbol contains hidden elements that hint at a personal cosmic message.")
    
    name = get_user_name()
    generate_sacred_symbol(name)

if __name__ == "__main__":
    main()