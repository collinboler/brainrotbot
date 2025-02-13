from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip, TextClip
from .captions import create_captions
import pysrt
import os
import re

def normalize_text(text):
    """Normalize text for comparison by removing special chars and converting numbers to words"""
    # Convert to lowercase and remove special characters
    text = text.lower()
    # Replace common variations
    replacements = {
        '(': '',
        ')': '',
        '[': '',
        ']': '',
        'f)': 'female',
        'm)': 'male',
        '20f': '20 female',
        '20m': '20 male',
        '(f)': 'female',
        '(m)': 'male',
        'f': 'female',
        'm': 'male',
        '&': 'and',
        '+': 'and',
        '/': ' ',
        '\\': ' ',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove any remaining special characters and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())

def find_title_end_index(subs, title_text):
    """Find the index of the subtitle that contains the end of the title"""
    # Normalize the title text
    clean_title = normalize_text(title_text)
    title_words = clean_title.split()
    
    # Build text progressively to find complete title
    combined_text = ""
    last_matching_idx = 0
    
    for i, sub in enumerate(subs):
        # Normalize the subtitle text
        word = normalize_text(sub.text)
        combined_text += word + " "
        
        # Check if we have the complete title
        if all(title_word in combined_text for title_word in title_words):
            return i
        
        # Update last matching index if we have a partial match
        for title_word in title_words:
            if title_word in word:
                last_matching_idx = i
    
    # If we didn't find the complete title, return the last matching index
    # or a reasonable minimum
    return max(last_matching_idx, min(8, len(subs) - 1))

def get_title_end_time(subs, title_end_idx):
    """Get the end time of the title in seconds"""
    if title_end_idx >= 0 and title_end_idx < len(subs):
        # Add a larger buffer to the end time
        return (subs[title_end_idx].end.ordinal / 1000) + 0.5  # Add 500ms buffer
    return 3.0  # Default to 3 seconds if title not found

def trim_and_join(base_video_path, base_audio_path, image_path, output, title_text=""):
    clip = VideoFileClip(f"{base_video_path}")
    audioclip = AudioFileClip(f"{base_audio_path}")

    # Generate captions first to get title timing
    srt_path = create_captions(base_audio_path)
    print("srt_path: " + srt_path)
    subs = pysrt.open(srt_path)
    print(f"Number of subtitles: {len(subs)}")
    
    # Find where the title ends in the subtitles
    title_end_idx = find_title_end_index(subs, title_text)
    print(f"Title ends at subtitle index: {title_end_idx}")
    
    # Get the exact time when title ends
    title_end_time = get_title_end_time(subs, title_end_idx)
    print(f"Title ends at: {title_end_time} seconds")

    # Create image clip that only shows during title
    image = ImageClip(f"{image_path}")
    image = image.with_duration(title_end_time).with_position(("center", "center"))

    # Trim video to match audio duration
    clip = clip.subclipped(end_time=audioclip.duration)
    clip.audio = CompositeAudioClip([audioclip])
    
    # Create text clips for each subtitle (skipping until after the title)
    txt_clips = []
    font_path = "Utils/Edit/Base/boldfont.ttf"
    
    # Calculate text width (80% of video width)
    text_width = int(clip.w * 0.8)
    
    # Process subtitles after the title
    for sub in subs[title_end_idx + 1:]:
        start_time = sub.start.ordinal / 1000  # Convert to seconds
        end_time = sub.end.ordinal / 1000
        duration = end_time - start_time
        
        # Create simple centered text clip
        txt_clip = TextClip(
            text=sub.text,
            font=font_path,
            font_size=65,
            color='white',
            stroke_color='black',
            stroke_width=4,
            size=(text_width, clip.h),  # Width fixed, height set to video height
            method='caption'
        ).with_duration(duration).with_start(start_time)
        
        # Center the text on screen
        txt_clip = txt_clip.with_position('center')
        txt_clips.append(txt_clip)

    # Combine all clips: background video, title image overlay, and text captions
    final = CompositeVideoClip([clip, image] + txt_clips, size=clip.size)

    output_path = output + '.mp4'
    final.write_videofile(output_path, fps=60)
    return output_path
    
    

# test purposes only
# trim_and_join(base_video_path='./Edit/Base/base_video.mp4', base_audio_path='./Assets/reddit_audio.wav', image_path='./Assets/reddit_screenshot.png', output='test')