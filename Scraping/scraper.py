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

def fetch_trending_posts(subreddit_name="all", limit=10):
    subreddit = reddit.subreddit(subreddit_name) #pass the sub name here
    trending_posts = []

    for post in subreddit.hot(limit=limit):
        post_data = {
             "title": post.title,
            "url": post.url,
            "score": post.score,
            "comments": post.num_comments,
            "author": str(post.author),
            "created_utc": post.created_utc
        } 
    
     # Get the text (self text) if it's a self-post (not a link post)
        if post.selftext:
            post_data["selftext"] = post.selftext
        else:
            post_data["selftext"] = "No text content (link post)"

        trending_posts.append(post_data)
    
    return trending_posts

# Fetch and display trending posts
if __name__ == "__main__":
    subreddit = "AmItheAsshole"
    posts = fetch_trending_posts(subreddit, 5)

    print(f"Trending posts from r/{subreddit}:\n")
    for i, post in enumerate(posts, 1):
        print(f"{i}. {post['title']} (Score: {post['score']})")
        print(f"   URL: {post['url']}")
        print(f"   Author: {post['author']} | Comments: {post['comments']}\n")
