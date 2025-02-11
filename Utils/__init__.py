import os
from Utils.Scraper.reddit_scraper import fetch_post
from Utils.Scraper.reddit_screenshot import take_reddit_screenshot
from Utils.Audio.google_tts.googleaudio import text_to_speech as google_tts
from Utils.Audio.eleven_labs.elevenaudio import text_to_speech as eleven_labs_tts
from Utils.Audio.openai_tts.openai_audio import text_to_speech as openai_tts
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
    get_audio(text, output_path='Assets/reddit_audio.wav', tts_service='openai', **kwargs):
        Converts the given text to speech using various TTS services.
    merge(audio_path, image_path, output_path, base_video_path='./Edit/Base/base_video.mp4'):
        Trims and joins the given video clips.
    """
    # Class variable to store voice preference
    voice_gender = None
    
    @staticmethod
    def ask_gender():
        """Ask for gender preference and return corresponding voice."""
        while True:
            gender = input("male (m) or female (f)? ").lower().strip()
            if gender in ['m', 'f']:
                BrainRotBot.voice_gender = 'ash' if gender == 'm' else 'sage'
                return BrainRotBot.voice_gender
            print("Please enter 'm' for male or 'f' for female.")

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
        # Ask for gender preference if not already set
        if BrainRotBot.voice_gender is None:
            BrainRotBot.ask_gender()
            
        return take_reddit_screenshot(post_url)
    
    @staticmethod
    def get_audio(text, output_path='Assets/reddit_audio.wav', tts_service='openai', **kwargs):
        """
        Converts the given text to speech using various TTS services.
        
        Parameters
        ----------
        text : str
            Text to convert to speech
        output_path : str, optional
            Path to save the audio file (default is 'Assets/reddit_audio.wav')
        tts_service : str, optional
            TTS service to use (default is 'openai')
            Options: 'google', 'elevenlabs', 'openai'
        **kwargs : dict
            Additional arguments for specific TTS services:
            - elevenlabs: voice_id (str)
            - openai: voice (str, either 'ash' or 'sage'), model (str, 'tts-1' or 'tts-1-hd')
        
        Returns
        -------
        str
            Path to the generated audio file
        """
        if tts_service == 'elevenlabs':
            return eleven_labs_tts(text, output=output_path, voice_id=kwargs.get('voice_id'))
        elif tts_service == 'openai':
            # Use the stored voice gender preference
            voice = kwargs.get('voice', BrainRotBot.voice_gender)
            return openai_tts(
                text, 
                output=output_path, 
                voice=voice,
                model=kwargs.get('model', 'tts-1')
            )
        else:  # default to google
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
    
    