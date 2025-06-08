import os
import time
import json
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import pygame
from openai import OpenAI
import tempfile
import wave
import struct

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Flag to track if speech recognition is available
SPEECH_RECOGNITION_AVAILABLE = False

# Try to import PyAudio - we'll just set the flag to False if it fails
try:
    import pyaudio  # type: ignore # Suppress Pylance warning
    p = pyaudio.PyAudio()
    SPEECH_RECOGNITION_AVAILABLE = True
    print("Speech recognition is available!")
except (ImportError, ModuleNotFoundError):
    print("PyAudio not installed. Running in text-only mode.")

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Cache for audio files to avoid regenerating common messages
audio_cache = {}

def record_audio(duration=5):
    """Record audio from the microphone if PyAudio is available."""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return None
    
    try:
        # Set recording parameters
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024
        
        # Start recording
        print("Recording... Speak now.")
        audio = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * duration)):
            data = audio.read(CHUNK)
            frames.append(data)
        
        print("Recording finished.")
        
        # Stop recording
        audio.stop_stream()
        audio.close()
        
        # Create a temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wf = wave.open(temp_file.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return temp_file.name
    
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

def transcribe_with_whisper(audio_file_path):
    """Transcribe audio using OpenAI's Whisper API."""
    if not audio_file_path:
        return None
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        # Delete the temporary file
        try:
            os.unlink(audio_file_path)
        except:
            pass
            
        return response.text
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def listen_for_name():
    """Listen for the user's name or get it via text input."""
    if SPEECH_RECOGNITION_AVAILABLE:
        print("\nPlease say your name clearly...")
        audio_file_path = record_audio(duration=3)
        if audio_file_path:
            name = transcribe_with_whisper(audio_file_path)
            if name:
                print(f"I heard your name as: {name}")
                return name.strip()
    
    # Fallback to text input if speech recognition failed or isn't available
    print("Please type your name:")
    return input("Your name: ")

def listen_to_speech():
    """Listen to the user's speech or get input via text."""
    if SPEECH_RECOGNITION_AVAILABLE:
        print("\nListening... (Speak your question about your past life)")
        audio_file_path = record_audio(duration=5)
        if audio_file_path:
            text = transcribe_with_whisper(audio_file_path)
            if text:
                print(f"You asked: {text}")
                return text.strip()
    
    # Fallback to text input if speech recognition failed or isn't available
    print("Please type your question about your past life:")
    question = input("Your question (or type 'exit' to quit): ")
    if question:
        print(f"You asked: {question}")
    return question

def generate_past_life_story(name):
    """Generate a story about the user's past life."""
    try:
        # Create a prompt for the story generation
        prompt = f"Create a brief, funny description (2-3 sentences) of who {name} was in their past life. Start with 'You were...' and include their occupation and one amusing detail. Be concise but humorous."
        
        # Generate the story using OpenAI's API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative storyteller specializing in brief, humorous past life narratives. Keep responses under 75 words."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.8
        )
        
        # Extract the story from the response
        story = response.choices[0].message.content.strip()
        
        print(f"\nGenerating a story about {name}'s past life...")
        print("\n" + story + "\n")
        
        return story
    
    except Exception as e:
        print(f"Error generating past life story: {e}")
        return f"You were a mysterious figure whose story has been lost to time."

def answer_past_life_question(name, story, question):
    """Generate an answer to a question about the user's past life."""
    try:
        # Create a prompt for answering the question
        prompt = f"""
        Based on this past life story about {name}:
        
        "{story}"
        
        Answer this question about their past life: "{question}"
        
        Be creative, entertaining, and consistent with the story. Keep your answer VERY BRIEF (1-3 sentences maximum). Be concise but include a humorous detail.
        """
        
        # Generate the answer using OpenAI's API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a mystical oracle who can see into people's past lives. You answer questions with brevity, humor, and confidence. Keep responses under 50 words."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=75,
            temperature=0.7
        )
        
        # Extract the answer from the response
        answer = response.choices[0].message.content.strip()
        
        print(f"\nOracle's answer:")
        print("\n" + answer + "\n")
        
        return answer
    
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "The mists of time obscure that detail of your past life. Ask another question."

def generate_audio_narration(text):
    """Generate audio narration for text with caching for common messages."""
    try:
        # Check if we already have this text in our cache
        if text in audio_cache:
            print("Using cached audio...")
            return audio_cache[text]
        
        print("Generating audio... (this may take a moment)")
        
        # Create output directory if it doesn't exist
        os.makedirs("output_audio", exist_ok=True)
        
        # Generate a timestamp for the filename
        timestamp = int(time.time())
        audio_path = f"output_audio/oracle_response_{timestamp}.mp3"
        
        # Generate audio using OpenAI's Text-to-Speech API
        # Use the faster tts-1-hd model for better performance
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Using a deep, dramatic voice for storytelling
            input=text,
            speed=1.1  # Slightly faster speech for better pacing
        )
        
        # Save the audio file
        with open(audio_path, 'wb') as f:
            for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                f.write(chunk)
        
        print(f"Audio narration has been generated and saved to {audio_path}")
        
        # Cache this audio for future use
        audio_cache[text] = audio_path
        
        return audio_path
    
    except Exception as e:
        print(f"Error generating audio narration: {e}")
        print("Continuing without audio...")
        return None

def play_audio(audio_path):
    """Play the generated audio file with optimized playback."""
    try:
        if audio_path and os.path.exists(audio_path):
            print(f"Playing audio narration...")
            
            # Use a separate channel for better performance
            sound = pygame.mixer.Sound(audio_path)
            channel = pygame.mixer.Channel(0)
            channel.play(sound)
            
            # Wait for the audio to finish playing with a more responsive loop
            while channel.get_busy():
                pygame.time.Clock().tick(30)  # Higher tick rate for more responsive UI
    
    except Exception as e:
        print(f"Error playing audio: {e}")
        print("Continuing without audio playback...")

def generate_past_life_face(name):
    """Generate an image of how the person looked in their past life."""
    # Create a more concise prompt for faster generation
    prompt = f"""Portrait of {name} in past life, realistic face, period clothing, simple background."""
    
    print("\nGenerating your past life appearance... (this may take a moment)")
    
    try:
        # Generate the image using DALL-E with optimized settings
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size="512x512"  # Smaller size for faster generation
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download the image
        print("Downloading image...")
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        # Create output directory if it doesn't exist
        os.makedirs("oracle_symbols", exist_ok=True)
        
        # Save the image with a timestamp to avoid overwriting
        timestamp = int(time.time())
        image_path = f"oracle_symbols/{name}_past_life_{timestamp}.png"
        image.save(image_path)
        
        print(f"Past life appearance has been saved to {image_path}")
        
        # Display the image if in an environment that supports it
        try:
            image.show()
        except Exception as e:
            print(f"Note: Could not display the image automatically. Please open {image_path} to view it.")
        
        return image_path
    
    except Exception as e:
        print(f"Error generating past life image: {e}")
        print("Continuing without image...")
        return None

def speak_welcome_message():
    """Generate and play a welcome message."""
    welcome_message = """
    Welcome to the Past Life Oracle with Voice Interaction. 
    I will reveal how you looked in your past life and tell your story.
    You will receive both a visual representation and an audio narration.
    After hearing your story, you can ask questions using your voice.
    Let's begin. Please say your name clearly.
    """
    
    # Generate audio for the welcome message
    audio_path = generate_audio_narration(welcome_message)
    
    # Play the welcome message
    if audio_path:
        play_audio(audio_path)

def main():
    """Main function to run the oracle."""
    if SPEECH_RECOGNITION_AVAILABLE:
        print("=== Past Life Oracle with Voice Interaction ===")
    else:
        print("=== Past Life Oracle (Text-Only Mode) ===")
    
    print("This oracle will reveal how you looked in your past life and tell your story.")
    print("You will receive both a visual representation and an audio narration.")
    
    # Pre-cache common messages
    common_messages = {
        "welcome": "Welcome to the Past Life Oracle. I will reveal how you looked in your past life and tell your story. Please say your name clearly.",
        "ask_question": "You can now ask questions about your past life or say exit to end the session.",
        "farewell": "Thank you for consulting the Past Life Oracle. Farewell!"
    }
    
    # Pre-generate audio for common messages
    for key, message in common_messages.items():
        if key not in audio_cache:
            audio_cache[key] = generate_audio_narration(message)
    
    # Play welcome message
    if "welcome" in audio_cache:
        play_audio(audio_cache["welcome"])
    
    # Get user's name through voice
    name = listen_for_name()
    
    # Start image generation in parallel with story generation
    print("\nGenerating your past life details...")
    
    # Generate a story about the past life
    story = generate_past_life_story(name)
    
    # Generate the past life face image
    image_path = generate_past_life_face(name)
    
    # Generate audio narration of the story
    audio_path = generate_audio_narration(story)
    
    # Play the audio narration
    if audio_path:
        play_audio(audio_path)
    
    # Voice interaction loop for follow-up questions
    print("\n=== Voice Interaction Mode ===")
    print("You can now ask questions about your past life using your voice.")
    print("For example: 'What skills did I have?' or 'Tell me about my relationships'")
    print("Say 'exit' or 'quit' to end the session.")
    
    # Use cached prompt for asking questions
    if "ask_question" in audio_cache:
        play_audio(audio_cache["ask_question"])
    
    # Limit the number of follow-up questions to prevent lag
    max_questions = 5
    question_count = 0
    
    while question_count < max_questions:
        # Listen for the user's question
        question = listen_to_speech()
        
        # Check if the user wants to exit
        if question and any(exit_word in question.lower() for exit_word in ["exit", "quit", "stop", "end"]):
            print("\nThank you for consulting the Past Life Oracle. Farewell!")
            
            # Use cached farewell message
            if "farewell" in audio_cache:
                play_audio(audio_cache["farewell"])
            
            break
        
        # If a question was recognized, answer it
        if question:
            # Generate an answer to the question
            answer = answer_past_life_question(name, story, question)
            
            # Generate audio narration of the answer
            answer_audio_path = generate_audio_narration(answer)
            
            # Play the audio narration
            if answer_audio_path:
                play_audio(answer_audio_path)
            
            question_count += 1
            
            # If we've reached the maximum number of questions
            if question_count >= max_questions:
                print("\nYou've reached the maximum number of questions for this session.")
                print("Thank you for consulting the Past Life Oracle. Farewell!")
                
                # Use cached farewell message
                if "farewell" in audio_cache:
                    play_audio(audio_cache["farewell"])
                
                break

if __name__ == "__main__":
    main()
