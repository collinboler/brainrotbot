from gtts import gTTS
import os
from ..text_preprocessor import preprocess_text

def text_to_speech(text, output='./Assets/reddit_audio.wav'):
    """
    Convert text to speech using Google's TTS API
    
    Parameters
    ----------
    text : str
        The text to convert to speech
    output : str, optional
        Path to save the audio file (default is './Assets/reddit_audio.wav')
        
    Returns
    -------
    str
        Path to the generated audio file
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output), exist_ok=True)
    
    # Preprocess the text
    processed_text = preprocess_text(text)
    
    try:
        # Create gTTS instance
        tts = gTTS(text=processed_text, lang='en', slow=False)
        
        # Save the audio file
        tts.save(output)
        
        return output
        
    except Exception as e:
        print(f"Error generating audio with Google TTS: {str(e)}")
        return None

# Only run this test if file is run directly
if __name__ == "__main__":
    text_to_speech("Hello, how are you doing today?") 