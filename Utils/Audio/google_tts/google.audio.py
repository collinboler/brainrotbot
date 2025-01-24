from gtts import gTTS

#function that converts text to speech
def text_to_speech(text, lang='en', output='Assets/audio.mp3'):
    tts = gTTS(text, lang=lang)
    tts.save(output)
    
# text_to_speech("Hello, how are you doing today?") this is a example