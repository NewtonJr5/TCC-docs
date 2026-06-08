from .reddit_client import client


async def fetch_comments(subreddit: str, post_id: str):
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"

    response = await client.get(url)

    response.raise_for_status()

    return response.json()