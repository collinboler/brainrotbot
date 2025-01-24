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

def fetch_trending_posts(subreddit_name="", no_of_posts=10):
    if not (10 <= no_of_posts <= 50):
        raise ValueError("Number of posts must be greater than 10 and less than 50")
    
    if not subreddit_name:
        print("Enter subreddit name from the options below or type your own:")
        print("Options: relationship_advice, AmItheAsshole, RelationshipMemes, AskMen, confession, AskReddit, funny, todayilearned, worldnews, movies")
        subreddit_name = input()  # pass the sub name here
    subreddit = reddit.subreddit(subreddit_name)

    trending_posts = []
    for post in subreddit.hot(limit=100):  # Fetch more posts to allow for random selection
        if post.is_self and not post.over_18 and len(post.selftext.split()) >= 50 and len(post.selftext.split()) < 250:  # Filter posts with selftext containing at least 50 words and exclude NSFW posts
            trending_posts.append(post)

    random.shuffle(trending_posts)  # Shuffle the posts to randomize the order
    selected_posts = trending_posts[:no_of_posts]  # Select the top n posts after shuffling

    print("\n\nTrending Posts: \n")
    for i, post in enumerate(selected_posts):
        title = post.title
        if len(title) > 100:  # Set character limit for titles
            title = title[:97] + "..."
        print(f"{i+1}: {title}")

    userChoice = selected_posts[int(input("\n\nEnter your choice: ")) - 1]

    return userChoice

# fetch_trending_posts() #lmao
