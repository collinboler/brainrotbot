from Utils.Scraper.reddit_scraper import fetch_trending_posts
from Utils.Scraper.reddit_screenshot import take_reddit_screenshot
from Utils.Audio.kokoro_tts.kokoro_audio import text_to_speech
from Utils.Edit.edit import trim_and_join

class BrainRotBot:
    """
    A bot that fetches trending posts, takes screenshots of Reddit posts, converts text to speech, 
    and trims and joins video clips.
    
    Methods
    -------
    get_posts(no_of_posts=10):
        Fetches trending posts from a source.
    get_screenshot(post_url):
        Takes a screenshot of a given Reddit post.
    get_audio(text, voice_name='am_adam', output_path='Assets/reddit_audio.wav'):
        Converts the given text to speech.
    merge(audio_path, image_path, output_path, base_video_path='./Edit/Base/base_video.mp4'):
        Trims and joins the given video clips.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_posts(subreddit_name="", no_of_posts=10):
        """
        Fetches trending posts from a specified subreddit.
        
        Parameters
        ----------
        subreddit_name : str
            Name of the subreddit to fetch posts from
        no_of_posts : int, optional
            Number of posts to fetch (default is 10)
        
        Returns
        -------
        list
            A list of trending posts
        """
        return fetch_trending_posts(subreddit_name, no_of_posts)

    @staticmethod
    def get_screenshot(post_url):
        """
        Takes a screenshot of a given Reddit post.
        
        Parameters
        ----------
        post_url : str
            URL of the Reddit post
        
        Returns
        -------
        str
            Path to the screenshot image
        """
        return take_reddit_screenshot(post_url)
    
    @staticmethod
    def get_audio(text, voice_name='am_adam', output_path='Assets/reddit_audio.wav'):
        """
        Converts the given text to speech.
        
        Parameters
        ----------
        text : str
            Text to convert to speech
        voice_name : str, optional
            Name of the voice to use (default is 'am_adam')
        output_path : str, optional
            Path to save the audio file (default is 'Assets/reddit_audio.wav')
        
        Returns
        -------
        str
            Path to the generated audio file
        """
        return text_to_speech(text, voice_name, output_path)
    
    @staticmethod
    def merge(audio_path, image_path, output_path, base_video_path='./Utils/Edit/Base/base_video.mp4'):
        """
        Trims and joins the given video clips.
        
        Parameters
        ----------
        audio_path : str
            Path to the audio file
        image_path : str
            Path to the image file
        output_path : str
            Path to save the output video
        base_video_path : str, optional
            Path to the base video file (default is './Edit/Base/base_video.mp4')
        
        Returns
        -------
        str
            Path to the merged video file
        """
        return trim_and_join(base_video_path, base_audio_path=audio_path, image_path=image_path, output=f'Results/{output_path}')
    
    