from Scraper.reddit_scraper import fetch_trending_posts 
from Scraper.reddit_screenshot import take_reddit_screenshot
from Audio.tiktok_tts.tiktok_audio import text_to_speech
from Edit.edit import trim_and_join
import re

def main():
    post = fetch_trending_posts()
    print(post.title)
    # print('\n\n' + post.selftext)
    
    take_reddit_screenshot(post.url)
    print("Screenshot taken")
    
    
    content = re.sub(r'[\n\(\)]', '.', post.selftext) # Remove newlines and brackets
    text_to_speech((post.title + ' . ' + content))
    # print("Audio generated")
    
main()

trim_and_join(
    base_video_path= "./BaseVideo/minecraft.mp4",
    base_audio_path= "./Assets/reddit_audio.mp3",
    image_path= "./Assets/post_screenshot.png",
    output= "finalvideo"
)