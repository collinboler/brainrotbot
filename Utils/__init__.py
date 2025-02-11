import os
from Utils.Scraper.reddit_scraper import fetch_post
from Utils.Scraper.reddit_screenshot import take_reddit_screenshot
from Utils.Audio.google_tts.googleaudio import text_to_speech as google_tts
from Utils.Audio.eleven_labs.elevenaudio import text_to_speech as eleven_labs_tts
from Utils.Edit.edit import trim_and_join

class BrainRotBot:
    """
    A bot that fetches trending posts, takes screenshots of Reddit posts, converts text to speech, 
    and trims and joins video clips.
    
    Methods
    -------
    get_post(no_of_posts=10):
        Fetches trending posts from a source.
    get_screenshot(post_url):
        Takes a screenshot of a given Reddit post.
    get_audio(text, voice_name='am_adam', output_path='Assets/reddit_audio.wav', use_eleven_labs=False):
        Converts the given text to speech using either Google TTS or Eleven Labs.
    merge(audio_path, image_path, output_path, base_video_path='./Edit/Base/base_video.mp4'):
        Trims and joins the given video clips.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_post(subreddit_name="", no_of_posts=10):
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
        return fetch_post(subreddit_name, no_of_posts)

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
    def get_audio(text, output_path='Assets/reddit_audio.wav', use_eleven_labs=True, voice_id=None):
        """
        Converts the given text to speech using either Google TTS or Eleven Labs.
        
        Parameters
        ----------
        text : str
            Text to convert to speech
        output_path : str, optional
            Path to save the audio file (default is 'Assets/reddit_audio.wav')
        use_eleven_labs : bool, optional
            Whether to use Eleven Labs instead of Google TTS (default is False)
        voice_id : str, optional
            Voice ID for Eleven Labs (only used if use_eleven_labs is True)
        
        Returns
        -------
        str
            Path to the generated audio file
        """
        if use_eleven_labs:
            return eleven_labs_tts(text, output=output_path, voice_id=voice_id)
        else:
            return google_tts(text, output=output_path)
    
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
        # Create Results directory if it doesn't exist
        os.makedirs('Results', exist_ok=True)
        return trim_and_join(base_video_path, base_audio_path=audio_path, image_path=image_path, output=f'Results/{output_path}')
    
    