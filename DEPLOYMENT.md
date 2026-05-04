# Vercel Deployment Guide

This guide explains how to deploy the Instagram bot to Vercel with scheduled cron jobs.

## Why Vercel?

Vercel provides:
- **Serverless Functions**: Run code without managing servers
- **Cron Jobs**: Schedule your bot to run automatically at specific times
- **Free Tier**: Good for hobby projects with reasonable limits
- **Easy Scaling**: Automatically scales with usage

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Instagram Account**: For testing purposes

## Deployment Steps

### 1. Push to GitHub

```bash
git add .
git commit -m "feat: prepare for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Select your GitHub repository
4. Click **"Import"**

### 3. Configure Environment Variables

In the Vercel dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:
   - `INSTAGRAM_USERNAME`: Your Instagram email/username
   - `INSTAGRAM_PASSWORD`: Your Instagram password
   - `BOT_API_KEY`: A secret token (optional, for security)

**⚠️ Security Note**: Never commit credentials to GitHub. Use Vercel's environment variables feature.

### 4. Configure Cron Schedule

The `vercel.json` file defines two daily schedules:

```json
"crons": [
  {
    "path": "/api/bot",
    "schedule": "0 9 * * *"    // 9:00 AM UTC
  },
  {
    "path": "/api/bot",
    "schedule": "0 15 * * *"   // 3:00 PM UTC
  }
]
```

**Cron Schedule Format**: `minute hour day_of_month month day_of_week`

#### Common Schedule Examples:
- `0 9 * * *` → 9:00 AM every day
- `0 15 * * *` → 3:00 PM every day
- `0 8,14,20 * * *` → 8:00 AM, 2:00 PM, 8:00 PM every day
- `0 9 * * 1-5` → 9:00 AM Monday-Friday
- `*/30 * * * *` → Every 30 minutes

To customize schedules, edit `vercel.json` and redeploy.

### 5. Deploy

```bash
git add vercel.json
git commit -m "chore: add Vercel cron configuration"
git push origin main
```

Vercel will automatically deploy when you push to GitHub.

## Monitoring

### View Logs

1. Go to your Vercel project dashboard
2. Click on **"Deployments"**
3. Select the latest deployment
4. View function logs in the **"Logs"** tab

### Test the Bot Manually

Send a POST request to trigger the bot:

```bash
# Using curl
curl -X POST https://your-project.vercel.app/api/bot \
  -H "x-api-key: your-secret-token"

# Using Python
import requests
response = requests.post(
    "https://your-project.vercel.app/api/bot",
    headers={"x-api-key": "your-secret-token"}
)
print(response.json())
```

## Verify Cron Jobs

Cron jobs are automatically enabled on Vercel Pro or with Hobby plan for public repos. 

To verify:
1. Go to project **Settings** → **Cron Jobs**
2. You should see your scheduled jobs listed

## Troubleshooting

### Bot Not Running

1. **Check logs**: View deployment logs in the Vercel dashboard
2. **Verify credentials**: Ensure `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` are set correctly
3. **Check rate limits**: Instagram may have blocked the account (anti-bot measures)

### Authentication Failures

If you see login errors:
- Verify credentials in Vercel environment variables
- Instagram may require 2FA setup
- Try logging in on Instagram's website to verify account status

### Rate Limiting

Instagram enforces strict rate limits. If you see rate limit errors:
- Reduce interaction probabilities in `api/bot.py`
- Increase delay times between actions
- Schedule fewer bot runs per day

## Advanced Configuration

### Change Interaction Probabilities

Edit `api/bot.py`:

```python
LIKE_PROBABILITY = 0.5      # 50%
FOLLOW_PROBABILITY = 0.75   # 75%
COMMENT_PROBABILITY = 0.10  # 10%
```

### Add Custom Tags or Comments

Edit `api/bot.py`:

```python
TAGS = ["pixelart", "gamedev", "indiegame", "pythoncoding"]
COMMENTS = ["Great work!", "Keep it up", "Nice", ":)"]
```

## Local Testing

Before deploying to Vercel, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python main.py
```

## Costs

Vercel's free tier includes:
- Up to 1,000 serverless function invocations/day
- Unlimited bandwidth
- Cron jobs (10 invocations/day free tier)

**Note**: If you need more frequent runs, consider upgrading to Pro ($20/month).

## Disable/Stop the Bot

To stop the bot from running:

1. Go to Vercel dashboard → **Settings** → **Cron Jobs**
2. Disable the scheduled jobs
3. Or delete the `crons` section from `vercel.json`

## Security Best Practices

1. ✅ Use environment variables for credentials
2. ✅ Never commit `.env` file
3. ✅ Use API key token for manual triggers
4. ✅ Regularly monitor logs for suspicious activity
5. ✅ Keep Instagram password strong and unique
6. ✅ Consider Instagram app passwords if available

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Cron Jobs**: https://vercel.com/docs/cron-jobs
- **Instagrapi**: https://github.com/adw0rd/instagrapi
