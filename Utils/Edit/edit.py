from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip, TextClip
from .captions import create_captions
import pysrt
import os

def trim_and_join(base_video_path, base_audio_path, image_path, output):
    clip = VideoFileClip(f"{base_video_path}")
    audioclip = AudioFileClip(f"{base_audio_path}")

    image = ImageClip(f"{image_path}")
    audio_duration = audioclip.duration
    
    image = image.with_duration(audio_duration).with_position(("center","center"))

    clip = clip.subclipped(end_time = audio_duration)

    new_audioclip = CompositeAudioClip([audioclip])
    clip.audio = new_audioclip

    # Generate captions
    srt_path = create_captions(base_audio_path)
    print("srt_path: " +  srt_path)
    subs = pysrt.open(srt_path)
    print(f"Number of subtitles: {len(subs)}")
    
    # Create text clips for each subtitle
    txt_clips = []
    font_path = "Utils/Edit/Base/boldfont.ttf"
    print("font_path: " + font_path)
    
    # Calculate text width as integer (80% of video width)
    text_width = int(clip.w * 0.8)
    
    for sub in subs:
        start_time = sub.start.ordinal / 1000  # Convert to seconds
        end_time = sub.end.ordinal / 1000
        duration = end_time - start_time
        
        print(f"Creating caption: '{sub.text}' from {start_time}s to {end_time}s")
        
        # Create text clip with correct parameter names and integer size
        txt_clip = TextClip(
            text=sub.text,
            size=(text_width, None),
            font_size=70,  # Increased font size
            color='white',
            stroke_color='black',
            stroke_width=4,  # Increased stroke width
            font=font_path,
            method='caption'  # This method should handle text centering
        ).with_start(start_time).with_duration(duration)
        
        # Position the text higher up from the bottom with explicit y coordinate
        y_position = int(clip.h * 0.7)  # 70% down from the top
        txt_clip = txt_clip.with_position(('center', y_position))
        txt_clips.append(txt_clip)

    print(f"Created {len(txt_clips)} text clips")
    
    # Combine all clips: background video, image overlay, and text captions
    final = CompositeVideoClip([clip, image] + txt_clips, size=clip.size)

    output_path = output + '.mp4'
    final.write_videofile(output_path, fps=60)
    return output_path
    
    

# test purposes only
# trim_and_join(base_video_path='./Edit/Base/base_video.mp4', base_audio_path='./Assets/reddit_audio.wav', image_path='./Assets/reddit_screenshot.png', output='test')