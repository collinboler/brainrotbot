from gtts import gTTS
import os

#function that converts text to speech
def text_to_speech(text, lang='en', output='Assets/audio.mp3'):
    # Create Assets directory if it doesn't exist
    os.makedirs(os.path.dirname(output), exist_ok=True)
    
    tts = gTTS(text, lang=lang)
    tts.save(output)
    return output

# Only run this test if file is run directly
if __name__ == "__main__":
    text_to_speech("Hello, how are you doing today?") 