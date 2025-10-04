"""
Configuration module for the Telegram bot.
Handles environment variables and default settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Admin configuration
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Default configuration values
DEFAULT_CONFIG = {
    "currency_symbol": "₦",
    "min_withdrawal": 1000,
    "daily_bonus": 100,
    "referral_reward": 50,
    "dice_cooldown": 300,  # 5 minutes in seconds
    "max_daily_rolls": 10
}

# Rate limiting
RATE_LIMIT = {
    "dice_roll": 300,  # 5 minutes
    "daily_bonus": 86400,  # 24 hours
    "withdrawal": 3600,  # 1 hour
}

# Game rewards
DICE_REWARDS = {
    1: 10,
    2: 20,
    3: 30,
    4: 40,
    5: 50,
    6: 100
}