# Phoenix Filter Bot - Deployment Guide

Complete setup instructions for deploying to Railway, Render, and Koyeb.

---

## I. Prerequisites

Before deploying, ensure you have:

1. **Telegram Bot Token** - From @BotFather
2. **Telegram API Credentials** - API_ID and API_HASH from telegram.org
3. **MongoDB Database** - Connection string from MongoDB Atlas or similar
4. **Channel IDs** - Your file channel and log channel IDs
5. **Admin IDs** - Your Telegram user ID and other admin IDs

---

## II. Environment Variables

All configuration is done via environment variables. Set these on your deployment platform:

### Required Variables

```
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id
API_HASH=your_api_hash
DATABASE_URI=mongodb+srv://user:password@cluster.mongodb.net/dbname
LOG_CHANNEL=-1002450940556
CHANNELS=-1002458488257
ADMINS=6304040346
OWNER_ID=6304040346
FORCE_SUB_CHANNEL=-1002533961050
```

### Optional Variables

```
BOT_USERNAME=ph0enix_web
FORCE_SUB_ENABLED=True
PM_SEARCH_ENABLED=True
RENAME_ENABLED=True
STREAM_ENABLED=True
SHORTLINK_ENABLED=True
PREMIUM_ENABLED=True
CLONE_ENABLED=True
AUTO_APPROVE_ENABLED=False
```

---

## III. Deployment to Railway

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub or email
3. Create a new project

### Step 2: Connect Repository

1. Click **New** → **GitHub Repo**
2. Connect your GitHub account
3. Select the `phoenix_filter_bot` repository
4. Click **Deploy**

### Step 3: Add Environment Variables

1. Go to **Variables** tab in your Railway project
2. Click **Add Variable**
3. Add all required environment variables from Section II
4. Click **Deploy**

### Step 4: Monitor Deployment

1. Check the **Deployments** tab
2. View logs to ensure bot starts successfully
3. Look for: `✅ Bot started successfully!`

---

## IV. Deployment to Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Create Web Service

1. Click **New +** → **Web Service**
2. Select your `phoenix_filter_bot` repository
3. Configure:
   - **Name**: `phoenix-filter-bot`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`

### Step 3: Add Environment Variables

1. Scroll to **Environment** section
2. Click **Add Environment Variable**
3. Add all variables from Section II
4. Click **Create Web Service**

### Step 4: Monitor Deployment

1. Check the **Logs** tab
2. Wait for build to complete
3. Verify bot is running

---

## V. Deployment to Koyeb

### Step 1: Create Koyeb Account

1. Go to [koyeb.com](https://koyeb.com)
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Create App

1. Click **Create App**
2. Select **GitHub**
3. Choose your `phoenix_filter_bot` repository
4. Configure:
   - **App name**: `phoenix-filter-bot`
   - **Builder**: `Dockerfile`
   - **Instance type**: `Standard`

### Step 3: Add Environment Variables

1. In **Environment variables** section
2. Click **Add variable**
3. Add all variables from Section II
4. Click **Create App**

### Step 4: Monitor Deployment

1. Check **Activity** tab
2. Wait for deployment to complete
3. Verify in logs

---

## VI. Getting Required Credentials

### Telegram Bot Token

1. Open Telegram
2. Search for **@BotFather**
3. Send `/newbot`
4. Follow prompts
5. Copy the token (e.g., `123456:ABC-DEF1234567890`)

### API ID and API Hash

1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in with your Telegram account
3. Go to **API development tools**
4. Create a new application
5. Copy **API ID** and **API Hash**

### MongoDB Connection String

1. Go to [mongodb.com](https://mongodb.com)
2. Create a free account
3. Create a new cluster
4. Go to **Connect** → **Connect your application**
5. Copy the connection string
6. Replace `<password>` with your database password

### Channel IDs

To get channel IDs:

1. Forward a message from the channel to **@userinfobot**
2. The bot will show you the channel ID (negative number)
3. Example: `-1002450940556`

---

## VII. Post-Deployment Setup

### 1. Verify Bot is Running

Send `/start` to your bot in Telegram. You should see a welcome message.

### 2. Index Files

Send `/index` in a group where the bot is an admin and has access to your file channel.

### 3. Configure Force Subscribe

Send `/fsub @your_channel` to add a Force Subscribe channel.

### 4. Test Search

Send a search query in the bot's DM to test search functionality.

### 5. Check Logs

Verify that activities are being logged to your LOG_CHANNEL.

---

## VIII. Troubleshooting

### Bot Not Starting

**Check:**
- All required environment variables are set
- `BOT_TOKEN` is correct
- Database connection string is valid
- Check deployment logs for errors

**Fix:**
- Verify credentials
- Restart the deployment
- Check MongoDB connection

### Search Not Working

**Check:**
- Files are indexed: `/index`
- `CHANNELS` variable contains correct channel ID
- Bot is admin in file channel

**Fix:**
- Run `/index` again
- Verify channel permissions
- Check database connection

### Force Subscribe Not Working

**Check:**
- `FORCE_SUB_ENABLED=True`
- `FORCE_SUB_CHANNEL` is set correctly
- Bot is admin in the channel

**Fix:**
- Verify bot permissions
- Check channel ID format
- Restart bot

### Database Connection Issues

**Check:**
- `DATABASE_URI` is correct
- MongoDB cluster allows connections
- Database user has correct permissions

**Fix:**
- Verify connection string
- Add IP to MongoDB whitelist
- Check database user permissions

---

## IX. Updating the Bot

To update after making changes:

1. Push changes to GitHub
2. Deployment platform will automatically rebuild
3. Monitor logs for successful deployment
4. Verify bot is running with `/start`

---

## X. Support

For issues or questions:

- Contact: **@ph0enix_web**
- Check logs for error messages
- Verify all environment variables are set correctly

---

## XI. Important Notes

- **Never commit `.env` files** - Always use environment variables
- **Keep credentials secure** - Don't share your BOT_TOKEN or DATABASE_URI
- **Monitor logs** - Check deployment logs regularly for errors
- **Test thoroughly** - Test all features before going live
- **Backup database** - Regularly backup your MongoDB data

---

**Phoenix Filter Bot** - Built with ❤️ by Manus AI
