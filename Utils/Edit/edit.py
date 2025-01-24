from moviepy import *



def trim_and_join(base_video_path, base_audio_path, image_path, output):

    clip = VideoFileClip(f"{base_video_path}")
    audioclip = AudioFileClip(f"{base_audio_path}")

    image = ImageClip(f"{image_path}")
    audio_duration = audioclip.duration
    
    image = image.with_duration(audio_duration).with_position(("center","center"))

    clip = clip.subclipped(end_time = audio_duration)

    new_audioclip = CompositeAudioClip([audioclip])
    clip.audio = new_audioclip

    final = CompositeVideoClip([clip, image])

    output_path = output + '.mp4'
    final.write_videofile(output_path, fps=60)
    return output_path
    
    

# test purposes only
# trim_and_join(base_video_path='./Edit/Base/base_video.mp4', base_audio_path='./Assets/reddit_audio.wav', image_path='./Assets/reddit_screenshot.png', output='test')