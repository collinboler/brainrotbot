from moviepy import *



def trim_and_join(base_video_path, base_audio_path,image_path, output):

    clip = VideoFileClip(f"{base_video_path}")
    audioclip = AudioFileClip(f"{base_audio_path}")


    image = ImageClip(f"{image_path}")
    audio_duration = audioclip.duration
    
    image = image.with_duration(audio_duration).with_position(("center","center"))

    

    clip = clip.subclipped(end_time = audio_duration)

    new_audioclip = CompositeAudioClip([audioclip])
    clip.audio = new_audioclip

    final = CompositeVideoClip([clip, image])

    print("From edit.py | trim_and_add")
    print("returnes clip with audio applied")

    final.write_videofile(f"./FinalRender/{output}.mp4")
    
