from Scraper.reddit_scraper import fetch_trending_posts 
from Scraper.reddit_screenshot import take_reddit_screenshot
from Audio.tiktok_tts.tiktok_audio import text_to_speech
from Edit.edit import trim_and_join
import re
import os
import shutil

def main():
    post = fetch_trending_posts()
    print(post.title)
    
    screenshot = take_reddit_screenshot(post.url)
    print("Screenshot taken")
    
    content = re.sub(r'[\n\(\)]', '.', post.selftext) # Remove newlines and brackets
    audio = text_to_speech((post.title + ' . ' + content))
    # print("Audio generated")
    
    
    #merged
    result = trim_and_join(base_video_path='./Edit/Base/minecraft.mp4', base_audio_path=audio, image_path=screenshot, output=f'{post.title}')
    print(f'Video saved to {result}')
    
    assets_folder = './Assets'

    if os.path.exists(assets_folder):
        shutil.rmtree(assets_folder)
        print(f'Deleted everything in the {assets_folder} folder')
    else:
        print(f'{assets_folder} folder does not exist')
main()

