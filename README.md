# Instagram Follower Bot

An automated Instagram bot that searches for posts by hashtags, interacts with them, and follows creators. Built with Python and [instagrapi](https://github.com/adw0rd/instagrapi).

## Features

- 🔍 Search posts by hashtags
- ❤️ Automatically like posts (configurable probability)
- 💬 Leave comments on posts (configurable probability)
- 👥 Follow post creators (configurable probability)
- 🕐 Schedule interactions at specific times
- 🔄 Random delays to avoid detection
- 📝 Detailed logging for monitoring

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd FollowerBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up credentials**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your Instagram credentials:
   ```
   INSTAGRAM_USERNAME=your_email@example.com
   INSTAGRAM_PASSWORD=your_password
   ```

## Configuration

Edit the settings in `main.py`:

```python
TAGS = ["pixelart", "gamedev", "indiegame", "pythoncoding"]  # Hashtags to search
COMMENTS = ["Great work!", "Keep it up", "Nice", ":)"]      # Comment options

LIKE_PROBABILITY = 0.5      # 50% chance to like
FOLLOW_PROBABILITY = 0.75   # 75% chance to follow
COMMENT_PROBABILITY = 0.10  # 10% chance to comment
```

## Usage

**Run once:**
```bash
python main.py
```

**Schedule to run daily** (uncomment the scheduler section in `main.py`):
```python
# The bot will run automatically at the scheduled times
```

## ⚠️ Disclaimer

- Use this bot responsibly and in compliance with Instagram's Terms of Service
- Instagram may ban accounts for bot activity
- Use appropriate delays to avoid rate limiting
- This is for educational purposes only

## Requirements

- Python 3.8+
- Instagram account (with strong credentials)
- See [requirements.txt](requirements.txt) for dependencies
