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
    
    # Get the directory of the audio file
    audio_dir = Path(audio_path).parent
    srt_path = audio_dir / "subtitles.srt"
    
    # Create SRT content word by word
    srt_content = []
    for i, word in enumerate(transcript.words, 1):
        start_time = format_time(word.start)
        end_time = format_time(word.end)
        srt_content.extend([
            str(i),
            f"{start_time} --> {end_time}",
            word.text,
            ""  # Empty line between entries
        ])
    
    # Write the subtitles to file
    with open(srt_path, "w", encoding='utf-8') as f:
        f.write("\n".join(srt_content))
    
    return str(srt_path)

def format_time(ms):
    """Convert milliseconds to SRT time format (HH:MM:SS,mmm)"""
    if ms is None:
        return "00:00:00,000"
        
    # Convert to seconds
    seconds = ms / 1000
    
    # Calculate hours, minutes, seconds, and milliseconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}" 