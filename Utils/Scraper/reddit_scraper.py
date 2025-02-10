import praw
from dotenv import load_dotenv
import os
import random

load_dotenv()  # loading the .env

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def fetch_post(subreddit_name="", no_of_posts=25):
    if not (10 <= no_of_posts <= 50):
        raise ValueError("Number of posts must be greater than 10 and less than 50")
    
    default_subreddits = ["relationship_advice", "AmItheAsshole", "RelationshipMemes", "AskMen", "confession"]
    
    while not subreddit_name:
        print("Enter subreddit name: ")
        print("Few options:")
        print("  ".join(default_subreddits))
        subreddit_name = input().strip()
        if not subreddit_name:
            print("Error: Subreddit name cannot be empty. Please try again.")
    
    subreddit = reddit.subreddit(subreddit_name)

    trending_posts = []
    for post in subreddit.hot(limit=100):  # Fetch more posts to allow for random selection
        if post.is_self and not post.over_18 and len(post.selftext.split()) >= 150 and len(post.selftext.split()) < 250:  # Filter posts with selftext containing at least 50 words and exclude NSFW posts
            trending_posts.append(post)

    if not trending_posts:
        print(f"No suitable posts found in r/{subreddit_name}. Please try another subreddit.")
        return fetch_post("", no_of_posts)  # Retry with empty subreddit name

    random.shuffle(trending_posts)  # Shuffle the posts to randomize the order
    selected_posts = trending_posts[:no_of_posts]  # Select the top n posts after shuffling

    print("\n\nTrending Posts: \n")
    for i, post in enumerate(selected_posts):
        title = post.title
        if len(title) > 100:  # Set character limit for titles
            title = title[:97] + "..."
        print(f"{i+1}: {title}")

    while True:
        try:
            choice = int(input("\n\nEnter your choice (1-{}): ".format(len(selected_posts))))
            if 1 <= choice <= len(selected_posts):
                return selected_posts[choice - 1]
            print(f"Please enter a number between 1 and {len(selected_posts)}")
        except ValueError:
            print("Please enter a valid number")

# fetch_trending_posts() #lmao
