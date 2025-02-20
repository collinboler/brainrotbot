import requests
import os
from dotenv import load_dotenv
from ..text_preprocessor import preprocess_text

load_dotenv()  # Load environment variables from .env file

ELEVEN_LABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')  # Default to Adam voice if not specified

def text_to_speech(text, output='./Assets/reddit_audio.wav', voice_id=None):
    """
    Convert text to speech using Eleven Labs API
    
    Parameters
    ----------
    text : str
        The text to convert to speech
    output : str, optional
        Path to save the audio file (default is './Assets/reddit_audio.wav')
    voice_id : str, optional
        The ID of the voice to use (defaults to environment variable or Adam voice)
        
    Returns
    -------
    str
        Path to the generated audio file
    """
    if not ELEVEN_LABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output), exist_ok=True)
    
    # Use provided voice_id or fall back to default
    voice_id = voice_id or VOICE_ID
    
    # Preprocess the text
    processed_text = preprocess_text(text)
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }
    
    data = {
        "text": processed_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save the audio file
        with open(output, 'wb') as f:
            f.write(response.content)
        
        return output
        
    except requests.exceptions.RequestException as e:
        print(f"Error generating audio with Eleven Labs: {str(e)}")
        return None 