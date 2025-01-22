import praw
from dotenv import load_dotenv
import os

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
    subreddit = reddit.subreddit(input()) #pass the sub name here    
    
    trending_posts = []
    for post in subreddit.hot(limit=5):
        trending_posts.append(post)

    print("\n\nTrending Posts: \n")
    for i, post in enumerate(trending_posts):
        print(f"{i+1}: {post.title}") 
        
    userChoice = trending_posts[int(input("Enter your choice: ")) - 1]
    
    return userChoice

# fetch_trending_posts() #lmao