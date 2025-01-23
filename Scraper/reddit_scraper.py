import praw
from dotenv import load_dotenv
import os
import random

load_dotenv() #loading the .env

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def fetch_trending_posts(subreddit_name="all"):
    print("Enter subreddit name: ")
    print("Few options:\nrelationship_advice    AmItheAsshole   RelationshipMemes   AskMen  confession")
    subreddit = reddit.subreddit(input())  # pass the sub name here

    trending_posts = []
    for post in subreddit.hot(limit=50):  # Fetch more posts to allow for random selection
        if post.is_self and len(post.selftext.split()) >= 50:  # Filter posts with selftext containing at least 50 words
            trending_posts.append(post)

    random.shuffle(trending_posts)  # Shuffle the posts to randomize the order
    selected_posts = trending_posts[:5]  # Select the top 5 posts after shuffling

    print("\n\nTrending Posts: \n")
    for i, post in enumerate(selected_posts):
        title = post.title
        if len(title) > 100:  # Set character limit for titles
            title = title[:97] + "..."
        print(f"{i+1}: {title}")

    userChoice = selected_posts[int(input("Enter your choice: ")) - 1]

    return userChoice

# fetch_trending_posts() #lmao