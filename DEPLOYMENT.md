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
git commit -m "feat: Vercel deployment fixes"
git push origin main
```

### 2. Connect to Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Select your GitHub repository
4. Click **"Import"**

### 3. Configure Environment Variables (IMPORTANT)

In the Vercel dashboard:

1. Go to your project **Settings** → **Environment Variables**
2. Add the following variables:
   - Name: `INSTAGRAM_USERNAME` → Value: Your Instagram email/username
   - Name: `INSTAGRAM_PASSWORD` → Value: Your Instagram password

⚠️ **CRITICAL**: Make sure these are set BEFORE deploying! The cron jobs won't work without these.

### 4. Verify Cron Jobs Configuration

1. Go to your project **Settings** → **Cron Jobs**
2. You should see two scheduled jobs:
   - **9:00 AM UTC** daily
   - **3:00 PM UTC** daily

If cron jobs don't appear, you may need a **Vercel Pro** account or check that your repo is public.

### 5. Deploy

```bash
git add .
git commit -m "chore: final Vercel deployment"
git push origin main
```

Vercel will automatically build and deploy when you push to GitHub.

## Customize Cron Schedule

Edit `vercel.json` to change when the bot runs:

```json
"crons": [
  {
    "path": "/api/bot",
    "schedule": "0 9 * * *"    // 9:00 AM UTC
  }
]
```

**Cron Schedule Format**: `minute hour day_of_month month day_of_week`

#### Common Examples:
- `0 9 * * *` → 9:00 AM every day
- `0 15 * * *` → 3:00 PM every day
- `0 8,14,20 * * *` → 8:00 AM, 2:00 PM, 8:00 PM
- `0 9 * * 1-5` → 9:00 AM Monday-Friday (weekdays)
- `*/30 * * * *` → Every 30 minutes

## Monitoring

### View Logs

1. Go to your Vercel project dashboard
2. Click **"Deployments"** tab
3. Click the latest deployment
4. Scroll down to **"Runtime Logs"** section
5. Click **"View Logs"** and search for bot execution

### Manual Testing

Send a test request to trigger the bot:

```bash
curl -X POST https://your-project.vercel.app/api/bot
```

Expected response:
```json
{
  "status": "success",
  "timestamp": "2026-05-05T09:00:00.123456",
  "interactions": {
    "liked": 2,
    "followed": 3,
    "commented": 1,
    "total": 4
  }
}
```

## Troubleshooting

### ❌ Cron Jobs Not Appearing

**Solutions:**
1. Check if repo is **public** (cron jobs require public repos on free tier)
2. Upgrade to **Vercel Pro** ($20/month)
3. Verify `vercel.json` has correct cron configuration
4. Redeploy: `git push origin main`

### ❌ Bot Not Running / Execution Fails

**Check logs:**
1. Vercel Dashboard → Deployments → Latest → Logs
2. Look for error messages

**Common issues:**
- **"Credentials not configured"** → Set `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` in Vercel Settings
- **"Authentication failed"** → Username/password is incorrect
- **Network timeout** → Instagram API unavailable or rate limited

### ❌ "Missing Dependencies" Error

Make sure `requirements.txt` includes all dependencies:
```
instagrapi>=2.0.0
python-dotenv>=0.19.0
```

Redeploy after updating.

### ❌ Rate Limiting / Too Many Requests

Instagram blocks bot activity. If you see rate limit errors:

**Solutions:**
1. **Reduce activity**: Edit `api/bot.py` and lower probabilities:
   ```python
   LIKE_PROBABILITY = 0.3      # Reduced from 0.5
   FOLLOW_PROBABILITY = 0.5    # Reduced from 0.75
   COMMENT_PROBABILITY = 0.05  # Reduced from 0.10
   ```
2. **Increase delays**: Increase sleep times in `random_delay()` function
3. **Run less often**: Reduce cron schedule to once daily instead of twice

### ❌ Instagram Account Blocked

If Instagram blocks your account:
1. Don't use the bot for 24-48 hours
2. Try logging in manually to verify account is accessible
3. Instagram may have detected bot activity (anti-bot protection)
4. Consider waiting longer between runs or reducing activity

## Configuration

### Edit Tags and Comments

In `api/bot.py`, customize what the bot interacts with:

```python
TAGS = ["pixelart", "gamedev", "indiegame", "pythoncoding"]
COMMENTS = ["Great work!", "Keep it up", "Nice", ":)"]
```

### Edit Interaction Probabilities

```python
LIKE_PROBABILITY = 0.5      # 50% chance to like each post
FOLLOW_PROBABILITY = 0.75   # 75% chance to follow each creator
COMMENT_PROBABILITY = 0.10  # 10% chance to comment on each post
```

Then commit and push changes:
```bash
git add api/bot.py
git commit -m "chore: update bot configuration"
git push origin main
```

## Costs

Vercel's pricing:
- **Free Tier**: Limited cron jobs (10 invocations/day)
- **Pro**: $20/month (unlimited cron jobs)

For daily bot runs:
- 2 runs/day = 10 cron invocations/day fits free tier
- More frequent runs require Pro

## Disable/Stop the Bot

### Option 1: Disable Cron Jobs

1. Vercel Dashboard → Settings → Cron Jobs
2. Toggle jobs OFF

### Option 2: Remove from Code

Edit `vercel.json` and remove the `"crons"` section:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "env": { ... }
  // Remove "crons" section
}
```

Then push to redeploy.

## Security Best Practices

1. ✅ **Never commit `.env` file** - It's in `.gitignore`
2. ✅ **Use Vercel's environment variables** for credentials
3. ✅ **Keep Instagram password strong and unique**
4. ✅ **Monitor logs for suspicious activity**
5. ✅ **Avoid excessive bot activity** (Instagram has anti-bot systems)
6. ✅ **Don't share environment variable values** with anyone
7. ✅ **Use a dedicated Instagram account** for the bot (don't use your personal account)

## Local Development

To test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
# INSTAGRAM_USERNAME=your_email@example.com
# INSTAGRAM_PASSWORD=your_password

# Run locally
python main.py
```

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Cron Jobs**: https://vercel.com/docs/cron-jobs
- **Instagrapi**: https://github.com/adw0rd/instagrapi
- **Contact Support**: https://vercel.com/support

## Summary Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project created and connected
- [ ] Environment variables set (`INSTAGRAM_USERNAME`, `INSTAGRAM_PASSWORD`)
- [ ] Cron jobs enabled in Vercel Settings
- [ ] Test deployment succeeded
- [ ] Logs show successful bot execution
- [ ] Cron jobs running on schedule
