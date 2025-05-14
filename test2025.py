import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

def ask_oracle(question: str) -> str:
    """
    Sends a question to OpenAI and returns a mystical oracle-style response.

    Args:
        question (str): The question to ask the Oracle.

    Returns:
        str: The Oracle's cryptic response.
    """
    try:
        # Define messages with system and user roles
        messages = [
            {
                "role": "system",
                "content": "You are an ancient oracle, shrouded in mystery. "
                           "You speak in riddles, cryptic wisdom, and poetic metaphors. "
                           "Never provide direct answers. Instead, guide seekers with enigmatic insights. "
                           "If asked about financial, medical, or legal matters, respond with: "
                           "'The fates are unclear. Seek wisdom beyond the veil.'"
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # Make a request to OpenAI's ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4",  # Use the appropriate model
            messages=messages,
            max_tokens=300,
            temperature=0.9  # Adjust for creativity
        )

        # Return the Oracle's response
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage when running the script directly
    while True:
        user_question = input("\nAsk the Oracle a question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            print("\nThe Oracle bids you farewell...")
            break
        
        response = ask_oracle(user_question)
        print(f"\n🔮 The Oracle speaks:\n{response}\n")