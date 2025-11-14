# Contributing to Phoenix Filter Bot

Thank you for your interest in contributing to Phoenix Filter Bot!

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/phoenix_filter_bot.git
cd phoenix_filter_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Run the Bot Locally

```bash
python bot.py
```

## Code Structure

```
phoenix_filter_bot/
├── bot.py                 # Main entry point
├── config.py              # Configuration management
├── database/
│   ├── __init__.py
│   └── models.py          # MongoDB models
├── handlers/
│   ├── commands.py        # Basic commands
│   ├── search_handlers.py # Search functionality
│   ├── admin_handlers.py  # Admin commands
│   ├── premium_handlers.py# Premium features
│   └── file_handlers.py   # File management
└── utils/
    ├── search.py          # Search engine
    ├── fsub.py            # Force Subscribe logic
    └── helpers.py         # Utility functions
```

## Adding New Features

### 1. Create a New Handler

Create a new file in `handlers/` directory:

```python
# handlers/my_feature.py
from pyrogram import Client, filters
from pyrogram.types import Message

async def handle_my_command(client: Client, message: Message):
    """Handle my new command"""
    await message.reply_text("Feature working!")

def setup_my_handlers(client: Client):
    @client.on_message(filters.command("mycommand"))
    async def my_cmd(client: Client, message: Message):
        await handle_my_command(client, message)
```

### 2. Register Handler in bot.py

```python
from handlers.my_feature import setup_my_handlers

# In PhoenixFilterBot.initialize():
setup_my_handlers(self.client)
```

### 3. Update todo.md

Add your feature to the todo list and mark as complete when done.

## Code Style

- Use meaningful variable and function names
- Add docstrings to all functions
- Keep functions focused and modular
- Use type hints where possible
- Comment complex logic

Example:

```python
async def search_files(query: str, limit: int = 10) -> List[dict]:
    """
    Search for files matching the query.
    
    Args:
        query: Search query string
        limit: Maximum number of results
    
    Returns:
        List of matching files
    """
    # Implementation here
    pass
```

## Testing

Before submitting changes:

1. Test locally with your bot
2. Test all related commands
3. Check error handling
4. Verify database operations
5. Test with different user types (admin, premium, regular)

## Commit Messages

Use clear, descriptive commit messages:

```
✨ Add new feature description
🐛 Fix bug description
📝 Update documentation
🔧 Refactor code
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Update todo.md with completed items
4. Commit with clear messages
5. Push to your fork
6. Create a Pull Request with description

## Reporting Issues

When reporting issues, include:

- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error logs (if applicable)
- Environment details

## Questions?

Contact: **@ph0enix_web**

---

Thank you for contributing to Phoenix Filter Bot! 🔥
