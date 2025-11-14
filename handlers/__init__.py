"""Handlers module for Phoenix Filter Bot"""

# Import all handlers here for easy access
from .commands import setup_command_handlers
from .filters import setup_filters
from .callbacks import setup_callback_handlers

__all__ = [
    "setup_command_handlers",
    "setup_filters",
    "setup_callback_handlers",
]
