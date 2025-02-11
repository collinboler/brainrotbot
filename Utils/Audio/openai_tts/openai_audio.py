import os
from dotenv import load_dotenv
from openai import OpenAI
import random

load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AVAILABLE_VOICES = ["ash", "sage"]

def text_to_speech(text, output='./Assets/reddit_audio.wav', voice=None, model="tts-1"):
    """
    Convert text to speech using OpenAI's TTS API
    
    Parameters
    ----------
    text : str
        The text to convert to speech
    output : str, optional
        Path to save the audio file (default is './Assets/reddit_audio.wav')
    voice : str, optional
        The voice to use (default is randomly chosen between "ash" and "sage")
        Options: "ash", "sage"
    model : str, optional
        The TTS model to use (default is "tts-1")
        Options: "tts-1", "tts-1-hd"
        
    Returns
    -------
    str
        Path to the generated audio file
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # If no voice specified or invalid voice provided, randomly choose between ash and sage
    if not voice or voice not in AVAILABLE_VOICES:
        voice = random.choice(AVAILABLE_VOICES)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output), exist_ok=True)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        # Create the speech
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # Save the audio file
        response.stream_to_file(output)
        
        return output
        
    except Exception as e:
        print(f"Error generating audio with OpenAI: {str(e)}")
        return None 