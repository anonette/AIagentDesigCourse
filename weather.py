import json
import datetime
import os
import pygame
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Define the weather tool schema for OpenAI function calling
# Simplified to only require location (date will always be today)
WEATHER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "getWeather",
        "description": "Get the current weather forecast for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name, e.g., London, New York, Tokyo"
                }
            },
            "required": ["location"]
        }
    }
}

def generate_speech(text: str) -> str:
    """
    Generate speech from text using OpenAI's Text-to-Speech API.
    
    Args:
        text: The text to convert to speech
        
    Returns:
        The path to the generated audio file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output_audio", exist_ok=True)
        
        # Generate a timestamp for the filename
        timestamp = int(datetime.datetime.now().timestamp())
        audio_path = f"output_audio/weather_response_{timestamp}.mp3"
        
        # Generate audio using OpenAI's Text-to-Speech API
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Using a deep, dramatic voice
            input=text
        )
        
        # Save the audio file
        with open(audio_path, 'wb') as f:
            for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                f.write(chunk)
        
        print(f"Audio response generated and saved to {audio_path}")
        return audio_path
    
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

def play_audio(audio_path: str) -> None:
    """
    Play the generated audio file.
    
    Args:
        audio_path: The path to the audio file
    """
    try:
        if audio_path and os.path.exists(audio_path):
            print("Playing audio response...")
            
            # Use a separate channel for better performance
            sound = pygame.mixer.Sound(audio_path)
            channel = pygame.mixer.Channel(0)
            channel.play(sound)
            
            # Wait for the audio to finish playing
            while channel.get_busy():
                pygame.time.Clock().tick(30)
    
    except Exception as e:
        print(f"Error playing audio: {e}")

def get_weather(location: str) -> str:
    """
    Simulated weather tool that returns weather information for a given location (always for today).
    
    Args:
        location: The city name
    
    Returns:
        A string with the weather forecast
    """
    try:
        # Get today's date
        today = datetime.datetime.now()
        date_str = today.strftime("%B %d")
        
        # Simulated response - in a real app, this would come from a weather API
        return f"The weather in {location} on {date_str} is sunny, 24°C."
    
    except Exception as e:
        return f"Error retrieving weather data: {str(e)}"

def chat_with_weather_function(user_message: str) -> Tuple[str, str]:
    """
    Use OpenAI's function calling API to process a user message and potentially call the weather function.
    
    Args:
        user_message: The user's message
        
    Returns:
        A tuple containing (text_response, audio_path)
    """
    try:
        # Step 1: Send the user message and tool definition to the API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can provide current weather information. Always assume the user is asking about today's weather."},
                {"role": "user", "content": user_message}
            ],
            tools=[WEATHER_TOOL_SCHEMA],
            tool_choice="auto"
        )
        
        # Get the assistant's response
        assistant_message = response.choices[0].message
        
        # Step 2: Check if the model wants to call a tool
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            # Process each tool call
            tool_responses = []
            
            for tool_call in assistant_message.tool_calls:
                # Extract tool call information
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Call the weather function (always for today)
                if function_name == "getWeather":
                    location = function_args.get("location")
                    
                    if location:
                        tool_result = get_weather(location)
                    else:
                        tool_result = "Error: Missing required parameter (location)"
                else:
                    tool_result = f"Error: Unknown function {function_name}"
                
                tool_responses.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_result
                })
            
            # Step 3: Send the tool results back to the API
            second_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that can provide current weather information. Always assume the user is asking about today's weather."},
                    {"role": "user", "content": user_message},
                    assistant_message,
                    *[{"role": "tool", "tool_call_id": resp["tool_call_id"], "name": resp["name"], "content": resp["content"]} for resp in tool_responses]
                ]
            )
            
            # Get the final text response
            text_response = second_response.choices[0].message.content
            
            # Generate speech from the text response
            audio_path = generate_speech(text_response)
            
            return text_response, audio_path
        else:
            # If no tool call was made, return the assistant's response directly
            text_response = assistant_message.content
            audio_path = generate_speech(text_response)
            
            return text_response, audio_path
    
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return error_message, None

def main():
    """
    Main function to demonstrate OpenAI's function calling with the weather tool and TTS.
    """
    print("=== OpenAI Function Calling with Weather Tool and Text-to-Speech ===")
    print("This demo shows how to use OpenAI's function calling API to get current weather information")
    print("and convert the response to speech using OpenAI's Text-to-Speech API.")
    print("\nExample queries:")
    print("- What's the weather in Tokyo?")
    print("- Is it raining in London?")
    print("- Should I bring a jacket to New York?")
    print("- Just type a city name to get the weather there")
    print("\nType 'exit' to quit.")
    
    # Simple chat loop
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        # If the user just entered a city name, format it as a weather question
        if len(user_input.split()) == 1 and not any(x in user_input.lower() for x in ["exit", "quit", "bye"]):
            user_input = f"What's the weather in {user_input}?"
        
        # Process with OpenAI function calling and TTS
        text_response, audio_path = chat_with_weather_function(user_input)
        print(f"\nAssistant: {text_response}")
        
        # Play the audio response
        if audio_path:
            play_audio(audio_path)

if __name__ == "__main__":
    main()
