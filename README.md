# Phoenix Filter Bot

A next-generation Telegram media distribution bot with advanced Force Subscribe, AI spell check, premium membership, and comprehensive admin controls.

Built on the VJ-FILTER-BOT architecture with enhanced features and flexible environment variable configuration.

## Features

- **Auto-Filter Search:** Search media files without command prefix
- **File Indexing:** Automatic indexing from designated channels
- **Force Subscribe:** Advanced dynamic and environment-based Force Subscribe system
- **Premium Membership:** Tiered access with referral tracking
- **Streaming:** Multi-player streaming support
- **Rename & Customize:** File renaming with custom captions and thumbnails
- **URL Shortener:** Integrated URL shortening for monetization
- **Admin Commands:** 60+ commands for complete bot management
- **Logging:** Comprehensive activity logging to designated channel
- **Bot Cloning:** Users can create their own bot instances

## Deployment

Supports deployment to:
- Railway
- Render
- Koyeb
- VPS (Docker)

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions.

## Configuration

All configuration is done via environment variables. No hardcoded values in the codebase.

### Required Variables

- `BOT_TOKEN` - Telegram bot token from BotFather
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `DATABASE_URI` - MongoDB connection string
- `LOG_CHANNEL` - Channel ID for logging
- `CHANNELS` - File channel IDs (space-separated)
- `ADMINS` - Admin user IDs (space-separated)
- `OWNER_ID` - Bot owner's Telegram user ID
- `FORCE_SUB_CHANNEL` - Primary Force Subscribe channel

### Optional Variables

- `BOT_USERNAME` - Your Telegram username
- Feature toggles (PM_SEARCH_ENABLED, RENAME_ENABLED, etc.)
- Custom service URLs and API keys

## Project Structure

```
phoenix_filter_bot/
├── bot.py                 # Main bot entry point
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── database/
│   ├── __init__.py
│   └── models.py          # Database models
├── handlers/
│   ├── __init__.py
│   ├── commands.py        # Command handlers
│   ├── filters.py         # Message filters
│   └── callbacks.py       # Callback handlers
├── utils/
│   ├── __init__.py
│   ├── search.py          # Search functionality
│   ├── fsub.py            # Force Subscribe logic
│   └── helpers.py         # Helper functions
└── plugins/
    ├── __init__.py
    └── (feature plugins)
```

## Getting Started

### Local Development

1. Clone the repository
2. Create a `.env` file with required variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python bot.py`

### Docker Deployment

```bash
docker build -t phoenix-filter-bot .
docker run --env-file .env phoenix-filter-bot
```

## Credits

- **Phoenix Filter Bot** - Built by Manus AI
- Based on VJ-FILTER-BOT architecture
- Contact: @ph0enix_web

## License

GNU AGPL 2.0 - See LICENSE file for details
