# Local development script
# For Vercel deployment, uses api/index.py (Flask app)

import logging
import sys
from api.index import run_bot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Main execution - Local development only
if __name__ == "__main__":
    try:
        logger.info("Starting bot (local mode)...")
        result = run_bot()
        logger.info(f"Result: {result}")
        
        if result.get("status") == "success":
            logger.info("Bot execution completed successfully")
            sys.exit(0)
        else:
            logger.error(f"Bot execution failed: {result.get('message', 'Unknown error')}")
            sys.exit(1)
    
    except Exception as e:
        logger.critical(f"Bot failed: {e}")
        sys.exit(1)