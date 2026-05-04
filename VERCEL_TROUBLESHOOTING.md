# Vercel Deployment Troubleshooting Quick Guide

## 🚀 Quick Fixes

### Problem: Deployment Fails Immediately
**Solution:**
1. Check Vercel dashboard for error messages
2. Verify `requirements.txt` has correct packages
3. Ensure Python version is compatible (3.8+)

```bash
# Rebuild and redeploy
git add .
git commit -m "fix: deployment"
git push origin main
```

---

### Problem: Cron Jobs Not Appearing in Vercel

**Most Common Cause:** Repository is **private**

**Solutions:**
1. **Make repo public**: GitHub Settings → Make public
2. **Or upgrade to Vercel Pro** ($20/month allows private repos with cron)
3. Redeploy after changing

**Verify:**
- Dashboard → Settings → Cron Jobs (should see your jobs)

---

### Problem: Bot Doesn't Run at Scheduled Time

**Check:**
1. Are cron jobs enabled? → Dashboard → Settings → Cron Jobs
2. Are environment variables set? → Settings → Environment Variables
   - `INSTAGRAM_USERNAME` ✓
   - `INSTAGRAM_PASSWORD` ✓

**Fix missing credentials:**
1. Go to Vercel project Settings
2. Environment Variables
3. Add both variables
4. Redeploy: `git push origin main`

---

### Problem: "Credentials not configured" Error

**This means:**
- Environment variables not set in Vercel
- OR bot code can't access them

**Fix:**
1. Vercel Dashboard → Settings → Environment Variables
2. Add exactly:
   - Name: `INSTAGRAM_USERNAME` → Your Instagram email/username
   - Name: `INSTAGRAM_PASSWORD` → Your Instagram password
3. Click Save
4. Redeploy

---

### Problem: "Authentication failed"

**This means:**
- Username/password is incorrect
- Instagram blocked the account
- Instagram requires 2FA verification

**Fix:**
1. Test credentials locally:
   ```bash
   python main.py
   ```
2. If it works locally but not on Vercel, check credentials are exact (copy-paste)
3. Log into Instagram manually to verify account works
4. If blocked, wait 24-48 hours

---

### Problem: Build Fails - "ModuleNotFoundError: instagrapi"

**Fix:**
1. Check `requirements.txt` exists and has:
   ```
   instagrapi>=2.0.0
   python-dotenv>=0.19.0
   ```
2. Redeploy

---

### Problem: Manual Test Works, But Cron Doesn't Run

**Check:**
1. Are cron jobs **enabled**? (not just configured)
2. Is repo **public** (free tier requirement)?
3. Check Vercel logs at scheduled time

**Verify cron configuration:**
```json
// vercel.json should have:
"crons": [
  {
    "path": "/api/bot",
    "schedule": "0 9 * * *"
  }
]
```

---

### Problem: Rate Limit / Too Many Requests Error

**Cause:** Instagram anti-bot protection

**Fix - Slow down the bot:**

Edit `api/bot.py`:
```python
# Reduce activity
LIKE_PROBABILITY = 0.3       # Was 0.5
FOLLOW_PROBABILITY = 0.5     # Was 0.75
COMMENT_PROBABILITY = 0.05   # Was 0.10

# Run once per day, not twice
# Remove one cron job from vercel.json
```

Commit and push:
```bash
git add api/bot.py vercel.json
git commit -m "reduce bot activity to avoid rate limits"
git push origin main
```

---

## 📋 Step-by-Step: Deploy from Scratch

1. **Push to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "bot ready for Vercel"
   git push origin main
   ```

2. **Make GitHub repo PUBLIC**
   - GitHub.com → Your repo → Settings → Change to public

3. **Create Vercel project**
   - https://vercel.com/new
   - Select your GitHub repo
   - Click Import

4. **Set environment variables**
   - Vercel Dashboard → Project Settings → Environment Variables
   - Add: `INSTAGRAM_USERNAME` = your email
   - Add: `INSTAGRAM_PASSWORD` = your password
   - Save

5. **Deploy**
   - Hit "Deploy" button (or push to GitHub to auto-deploy)

6. **Verify cron jobs**
   - Dashboard → Settings → Cron Jobs
   - Should see 2 jobs listed

7. **Test manually**
   ```bash
   curl https://your-project.vercel.app/api/bot
   ```

8. **Check logs**
   - Dashboard → Deployments → Latest
   - Scroll to Runtime Logs

---

## 🔍 Useful Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **View your project**: https://your-project.vercel.app
- **Vercel Docs**: https://vercel.com/docs
- **Cron Job Format**: https://vercel.com/docs/cron-jobs

---

## 📞 Still Stuck?

1. **Check Vercel logs**
   - Most errors are in the Runtime Logs
   
2. **Test locally first**
   ```bash
   python main.py
   ```
   
3. **Verify your credentials work**
   - Can you log into Instagram.com with them?
   
4. **Check if Instagram blocked you**
   - Try logging in manually
   - Instagram may detect bot activity

5. **Contact Vercel Support**
   - https://vercel.com/support
