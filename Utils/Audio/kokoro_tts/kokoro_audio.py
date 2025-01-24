from gradio_client import Client, handle_file
import shutil
import dotenv
import os 

dotenv.load_dotenv()

KOKORO_CLIENT = os.getenv("KOKORO_CLIENT")

# Initialize the client
client = Client(KOKORO_CLIENT)

def text_to_speech(text_input, voice_name='am_adam', output_path='Assets/reddit_audio.wav'):
    result = client.predict(
        text=text_input,
        model_name="kokoro-v0_19.pth",
        voice_name=voice_name,
        speed=1,
        pad_between_segments=0,
        remove_silence=False,
        minimum_silence=0,
        custom_voicepack=None,
        api_name="/text_to_speech"
    )
    
    # Move the result file to the destination output_path
    shutil.move(result, output_path)
    return output_path
