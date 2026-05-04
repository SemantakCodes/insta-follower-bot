"""
Vercel serverless function for Instagram bot
Triggered by cron jobs defined in vercel.json
"""

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, RateLimitError
import random as r
import time
import logging
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load credentials from environment variables
load_dotenv()

# Configuration
TAGS = ["pixelart", "gamedev", "indiegame", "pythoncoding"]
COMMENTS = ["Great work!", "Keep it up", "Nice", ":)"]

# Probability settings (0.0 to 1.0)
LIKE_PROBABILITY = 0.5
FOLLOW_PROBABILITY = 0.75
COMMENT_PROBABILITY = 0.10


def random_delay(min_ms=2000, max_ms=7000):
    """Helper to apply random delay in milliseconds"""
    time.sleep(r.randint(min_ms, max_ms) / 1000)


def run_bot():
    """Execute bot interaction logic"""
    client = None
    
    # Get credentials
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    # Validate credentials
    if not username or not password:
        logger.error("Missing INSTAGRAM_USERNAME or INSTAGRAM_PASSWORD in environment variables")
        return {"status": "error", "message": "Credentials not configured"}
    
    try:
        # Initialize client
        client = Client()
        client.login(username, password)
        logger.info("Successfully logged in to Instagram")
        
        num_interaction_posts = r.randint(1, 5)
        
        # Search for posts
        random_delay(2000, 7000)
        tag_choice = r.choice(TAGS)
        hashtag_posts = client.hashtag_medias_recent(tag_choice)
        
        logger.info(f"Searched TAG ({tag_choice})")
        logger.info(f"Proceeding to interact with {num_interaction_posts} posts")
        
        # Select random posts without duplicates
        num_available = min(num_interaction_posts, len(hashtag_posts))
        if num_available == 0:
            logger.warning(f"No posts found for tag {tag_choice}")
            return {"status": "no_posts", "tag": tag_choice}
        
        chosen_post_indices = r.sample(range(len(hashtag_posts)), num_available)
        
        interactions_count = {
            "liked": 0,
            "followed": 0,
            "commented": 0,
            "total": len(chosen_post_indices)
        }
        
        # Interact with each post
        for idx in chosen_post_indices:
            post = hashtag_posts[idx]
            logger.info(f"Interacting with POST: '{post.caption_text[:50]}...'")
            
            # Determine actions based on probabilities
            like = r.random() < LIKE_PROBABILITY
            follow = r.random() < FOLLOW_PROBABILITY
            comment = r.random() < COMMENT_PROBABILITY
            
            media_id = post.pk
            user_id = post.user.pk
            
            random_delay(4000, 8000)
            
            # Try LIKE
            if like:
                random_delay(2000, 7000)
                try:
                    client.media_like(media_id)
                    logger.info("Post LIKED")
                    interactions_count["liked"] += 1
                except RateLimitError:
                    logger.warning("Rate limited on likes, skipping")
                except Exception as e:
                    logger.error(f"Failed to like post: {e}")
            
            # Try FOLLOW
            if follow:
                random_delay(3000, 9000)
                try:
                    client.user_follow(user_id)
                    logger.info("User FOLLOWED")
                    interactions_count["followed"] += 1
                except RateLimitError:
                    logger.warning("Rate limited on follows, skipping")
                except Exception as e:
                    logger.error(f"Failed to follow user: {e}")
            
            # Try COMMENT
            if comment:
                random_delay(7000, 12000)
                try:
                    client.media_comment(media_id, r.choice(COMMENTS))
                    logger.info("Post COMMENTED")
                    interactions_count["commented"] += 1
                except RateLimitError:
                    logger.warning("Rate limited on comments, skipping")
                except Exception as e:
                    logger.error(f"Failed to comment on post: {e}")
        
        logger.info(f"Interactions complete: {interactions_count}")
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "interactions": interactions_count
        }
    
    except LoginRequired:
        logger.error("Login failed. Check credentials.")
        return {"status": "error", "message": "Authentication failed"}
    except Exception as e:
        logger.error(f"Error in bot execution: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        if client:
            try:
                client.logout()
            except Exception as e:
                logger.warning(f"Error logging out: {e}")


# Vercel serverless function handler
def handler(request):
    """
    Handler for Vercel serverless function
    Triggered by cron jobs defined in vercel.json
    """
    try:
        # Log the request
        logger.info(f"Bot execution triggered at {datetime.now().isoformat()}")
        
        # Run the bot
        result = run_bot()
        
        # Vercel cron jobs expect JSON response
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }
    
    except Exception as e:
        logger.critical(f"Handler error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": str(e)})
        }
