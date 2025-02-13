import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1' # Prevents writing pycache files

from Utils import BrainRotBot
import re
import shutil
import sys

def main():
    # Getting the Post
    post = BrainRotBot.get_post(no_of_posts=25)
    print(post.title)
    
    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console
    
    # Getting the Screenshot
    screenshot = BrainRotBot.get_screenshot(post.url)
    if screenshot is None:
        print("\nFailed to capture screenshot. Exiting...")
        sys.exit(1)
    print("\nScreenshot taken!")    
    
    # Getting the Audio 
    cleaned_title = re.sub(r'[^\w\s]', '', post.title)
    audio = BrainRotBot.get_audio(post.title + post.selftext)
    print("\nAudio generated!")    
    
    # Merging the Video
    result = BrainRotBot.merge(audio, screenshot, cleaned_title, post.title)
    
    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console
    
    print(f'\nVideo saved to {result}')
    
    assets_folder = './Assets'

    if os.path.exists(assets_folder):
        shutil.rmtree(assets_folder)
        print(f'Deleted everything in the {assets_folder} folder')
    else:
        print(f'{assets_folder} folder does not exist')
        
main()

