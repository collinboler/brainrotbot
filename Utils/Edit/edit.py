from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip, TextClip
from .captions import create_captions
import pysrt
import os

def trim_and_join(base_video_path, base_audio_path, image_path, output):
    clip = VideoFileClip(f"{base_video_path}")
    audioclip = AudioFileClip(f"{base_audio_path}")

    image = ImageClip(f"{image_path}")
    audio_duration = audioclip.duration
    
    image = image.with_duration(audio_duration).with_position(("center", clip.h * 1/3))

    clip = clip.subclipped(end_time = audio_duration)

    new_audioclip = CompositeAudioClip([audioclip])
    clip.audio = new_audioclip

    # Generate captions
    srt_path = create_captions(base_audio_path)
    print("srt_path: " + srt_path)
    subs = pysrt.open(srt_path)
    print(f"Number of subtitles: {len(subs)}")
    
    # Create text clips for each subtitle
    txt_clips = []
    font_path = "Utils/Edit/Base/boldfont.ttf"
    
    # Calculate text width (80% of video width)
    text_width = int(clip.w * 0.8)
    
    for sub in subs:
        start_time = sub.start.ordinal / 1000  # Convert to seconds
        end_time = sub.end.ordinal / 1000
        duration = end_time - start_time
        
        # Create simple centered text clip
        txt_clip = TextClip(
            text=sub.text,
            font=font_path,
            font_size=70,
            color='white',
            stroke_color='black',
            stroke_width=4,
            size=(text_width, None),  # Width fixed, height automatic
            method='caption'
        ).with_duration(duration).with_start(start_time)
        
        # Center the text on screen
        txt_clip = txt_clip.with_position('center')
        txt_clips.append(txt_clip)

    # Combine all clips: background video, image overlay, and text captions
    final = CompositeVideoClip([clip, image] + txt_clips, size=clip.size)

    output_path = output + '.mp4'
    final.write_videofile(output_path, fps=60)
    return output_path
    
    

# test purposes only
# trim_and_join(base_video_path='./Edit/Base/base_video.mp4', base_audio_path='./Assets/reddit_audio.wav', image_path='./Assets/reddit_screenshot.png', output='test')