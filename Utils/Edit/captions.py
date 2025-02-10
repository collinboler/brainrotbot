import assemblyai as aai
import os
from pathlib import Path

def create_captions(audio_path):
    """
    Creates captions for the given audio file using AssemblyAI
    Returns the path to the generated SRT file
    """
    # Initialize AssemblyAI with the API key from environment
    aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
    
    # Create the transcription
    transcript = aai.Transcriber().transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt(chars_per_caption=15)
    
    # Get the directory of the audio file
    audio_dir = Path(audio_path).parent
    srt_path = audio_dir / "subtitles.srt"
    
    # Write the subtitles to file
    with open(srt_path, "w", encoding='utf-8') as f:
        f.write(subtitles)
    
    return str(srt_path) 