"""
Handler modules for the Telegram bot.
"""
from .user import register_user_handlers
from .admin import register_admin_handlers
from .games import register_game_handlers
from .withdraw import register_withdrawal_handlers

__all__ = ["register_user_handlers", "register_admin_handlers", "register_game_handlers", "register_withdrawal_handlers"]