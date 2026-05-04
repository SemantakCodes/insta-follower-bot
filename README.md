# Instagram Follower Bot

An automated Instagram bot that searches for posts by hashtags, interacts with them, and follows creators. Built with Python and [instagrapi](https://github.com/adw0rd/instagrapi).

Deployable to **Vercel** with automatic cron-based scheduling ⚡

## Features

- 🔍 Search posts by hashtags
- ❤️ Automatically like posts (configurable probability)
- 💬 Leave comments on posts (configurable probability)
- 👥 Follow post creators (configurable probability)
- ⏰ Schedule with Vercel cron jobs (serverless)
- 🔄 Random delays to avoid detection
- 📝 Detailed logging for monitoring

## Quick Start

### Local Development

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
   Edit `.env` with your Instagram credentials

4. **Run the bot**
   ```bash
   python main.py
   ```

### Deploy to Vercel (Recommended)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete Vercel setup instructions.

Quick overview:
1. Push to GitHub
2. Connect to Vercel (1 click)
3. Add environment variables
4. Bot runs automatically on schedule (cron jobs)

## Configuration

Edit settings in `api/bot.py`:

```python
TAGS = ["pixelart", "gamedev", "indiegame", "pythoncoding"]  # Hashtags to search
COMMENTS = ["Great work!", "Keep it up", "Nice", ":)"]      # Comment options

LIKE_PROBABILITY = 0.5      # 50% chance to like
FOLLOW_PROBABILITY = 0.75   # 75% chance to follow
COMMENT_PROBABILITY = 0.10  # 10% chance to comment
```

## Scheduling

The bot runs on two schedules by default (see `vercel.json`):
- **9:00 AM UTC** daily
- **3:00 PM UTC** daily

Customize cron schedules in `vercel.json` or `DEPLOYMENT.md`.

## Project Structure

```
.
├── api/
│   ├── __init__.py
│   └── bot.py              # Vercel serverless function
├── main.py                 # Local development script
├── requirements.txt        # Python dependencies
├── .env.example            # Credentials template
├── vercel.json             # Vercel configuration + cron jobs
├── README.md               # This file
├── DEPLOYMENT.md           # Vercel deployment guide
└── .gitignore              # Git ignore rules
```

## Requirements

- Python 3.8+ (local development)
- Instagram account
- See [requirements.txt](requirements.txt) for dependencies

## ⚠️ Disclaimer

- Use this bot responsibly and in compliance with Instagram's Terms of Service
- Instagram actively blocks bot activity - your account may be banned
- Use appropriate delays to avoid rate limiting
- This is for **educational purposes only**
- Consider the ethical implications of automation

## Security

- Never commit `.env` file (use `.gitignore`)
- Use environment variables for credentials
- Keep Instagram password strong and unique
- Monitor logs for suspicious activity

## Troubleshooting

**Bot not running?**
- Check Vercel logs: Dashboard → Deployments → Logs
- Verify credentials in environment variables
- Instagram may have security blocks

**Rate limit errors?**
- Reduce interaction probabilities
- Increase delay times
- Schedule fewer runs per day

See [DEPLOYMENT.md](DEPLOYMENT.md) for more troubleshooting tips.

## References

- [Vercel Docs](https://vercel.com/docs)
- [Vercel Cron Jobs](https://vercel.com/docs/cron-jobs)
- [Instagrapi Library](https://github.com/adw0rd/instagrapi)
