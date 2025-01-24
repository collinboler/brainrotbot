from Scraper.reddit_scraper import fetch_trending_posts 
from Scraper.reddit_screenshot import take_reddit_screenshot
# from Audio.tiktok_tts.tiktok_audio import text_to_speech
from Audio.kokoro_tts.kokoro_audio import text_to_speech

from Edit.edit import trim_and_join
import re
import os
import shutil

def main():
    post = fetch_trending_posts()
    print(post.title)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    screenshot = take_reddit_screenshot(post.url)
    print("Screenshot taken")
    
    title = re.sub(r'[^\w\s]', '', post.title) # Remove special characters
    content = re.sub(r'[\n\(\)]', '.', post.selftext) # Remove newlines and brackets
    audio = text_to_speech(text_input=(title + ' . ' + content))
    # print("Audio generated")
    
    
    #merged
    cleaned_title = re.sub(r'[^\w\s]', '', title)
    cleaned_title = ''.join(word.capitalize() for word in cleaned_title.split())
    result = trim_and_join(base_video_path='./Edit/Base/base_video.mp4', base_audio_path=audio, image_path=screenshot, output=f'{cleaned_title}')
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f'Video saved to {result}')
    
    assets_folder = './Assets'

    if os.path.exists(assets_folder):
        shutil.rmtree(assets_folder)
        print(f'Deleted everything in the {assets_folder} folder')
    else:
        print(f'{assets_folder} folder does not exist')
main()

