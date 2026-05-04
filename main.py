# Import needed libraries
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, RateLimitError
import random as r
import time
import schedule
import logging
import os
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load credentials from environment variables
load_dotenv()
USERNAME = os.getenv("INSTAGRAM_USERNAME", "email")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "password")

# Configuration
TAGS = ["pixelart", "gamedev", "indiegame", "pythoncoding"]
COMMENTS = ["Great work!", "Keep it up", "Nice", ":)"]

# Probability settings (0.0 to 1.0)
LIKE_PROBABILITY = 0.5
FOLLOW_PROBABILITY = 0.75
COMMENT_PROBABILITY = 0.10

# Global client instance
client = None

def initialize_client():
    """Initialize and authenticate the Instagram client once"""
    global client
    try:
        client = Client()
        client.login(USERNAME, PASSWORD)
        logger.info("Successfully logged in to Instagram")
    except LoginRequired:
        logger.error("Login failed. Check credentials.")
        raise
    except Exception as e:
        logger.error(f"Connection error: {e}")
        raise

def random_delay(min_ms=2000, max_ms=7000):
    """Helper to apply random delay in milliseconds"""
    time.sleep(r.randint(min_ms, max_ms) / 1000)

def search_tags():
    """Search for posts with certain tags and interact with them"""
    global client
    
    if client is None:
        initialize_client()
    
    try:
        num_interaction_posts = r.randint(1, 5)
        
        # Search for posts
        random_delay(2000, 7000)
        tag_choice = r.choice(TAGS)
        hashtag_posts = client.hashtag_medias_recent(tag_choice)
        
        logger.info(f"Searched TAG ({tag_choice})")
        logger.info(f"Proceeding to interact with {num_interaction_posts} posts")
        
        # Select random posts without duplicates
        num_available = min(num_interaction_posts, len(hashtag_posts))
        chosen_post_indices = r.sample(range(len(hashtag_posts)), num_available)
        
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
                except RateLimitError:
                    logger.warning("Rate limited on comments, skipping")
                except Exception as e:
                    logger.error(f"Failed to comment on post: {e}")
    
    except Exception as e:
        logger.error(f"Error in search_tags: {e}")
        raise


# Main execution
if __name__ == "__main__":
    try:
        # Initialize client once at startup
        initialize_client()
        
        # Option 1: Run once
        search_tags()
        
        # Option 2: Schedule to run at specific times (uncomment to use)
        # time_1 = f"{r.randint(8, 11)}:{r.randint(0, 59):02d}"
        # time_2 = f"{r.randint(13, 15)}:{r.randint(0, 59):02d}"
        # 
        # schedule.every().day.at(time_1).do(search_tags)
        # schedule.every().day.at(time_2).do(search_tags)
        # 
        # logger.info(f"Scheduled bot to run at {time_1} and {time_2}")
        # 
        # # Keep the script running indefinitely
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)
    
    except Exception as e:
        logger.critical(f"Bot failed: {e}")
        exit(1)