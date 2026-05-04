"""
Vercel serverless function for Instagram bot
Triggered by cron jobs defined in vercel.json
"""

from flask import Flask, jsonify, Request
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, RateLimitError
import random as r
import time
import logging
import os
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

# Initialize Flask app
app = Flask(__name__)


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
        logger.info("Initializing Instagram client...")
        client = Client()
        logger.info(f"Logging in as {username}...")
        client.login(username, password)
        logger.info("Successfully logged in to Instagram")
        
        num_interaction_posts = 7
        logger.info(f"Will interact with {num_interaction_posts} posts")
        
        # Search for posts
        random_delay(2000, 7000)
        tag_choice = r.choice(TAGS)
        logger.info(f"Searching for posts with tag: {tag_choice}")
        hashtag_posts = client.hashtag_medias_recent(tag_choice)
        logger.info(f"Found {len(hashtag_posts)} posts with tag {tag_choice}")
        
        # Select random posts without duplicates
        num_available = min(num_interaction_posts, len(hashtag_posts))
        if num_available == 0:
            logger.warning(f"No posts found for tag {tag_choice}")
            return {"status": "no_posts", "tag": tag_choice}
        
        chosen_post_indices = r.sample(range(len(hashtag_posts)), num_available)
        logger.info(f"Selected {num_available} random posts to interact with")
        
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
                logger.info("Logged out from Instagram")
            except Exception as e:
                logger.warning(f"Error logging out: {e}")


# Flask route for cron jobs
@app.route("/api/bot", methods=["GET", "POST"])
def bot_endpoint():
    """
    HTTP endpoint for cron jobs and manual triggers
    """
    logger.info("=" * 50)
    logger.info(f"Bot endpoint called at {datetime.now().isoformat()}")
    logger.info("=" * 50)
    
    try:
        result = run_bot()
        logger.info(f"Bot result: {result}")
        return jsonify(result), 200
    except Exception as e:
        logger.critical(f"Endpoint error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


# Health check endpoint
@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200


# Root endpoint
@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return jsonify({"message": "FollowerBot is running", "endpoints": {"/api/health": "Health check", "/api/bot": "Run bot"}}), 200


if __name__ == "__main__":
    logger.info("Starting Flask app...")
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
