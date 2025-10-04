"""
Helper functions for the Telegram bot.
"""
from datetime import datetime, timedelta
from config import ADMIN_ID


def format_currency(amount: float, currency_symbol: str = "₦") -> str:
    """Format amount with currency symbol."""
    return f"{currency_symbol}{amount:,.2f}"


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    if not dt:
        return "Never"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return user_id == ADMIN_ID


def can_roll_dice(user, cooldown_seconds: int = 300) -> tuple[bool, str]:
    """Check if user can roll dice."""
    if not user.last_dice_roll:
        return True, ""
    
    time_since_last_roll = datetime.utcnow() - user.last_dice_roll
    if time_since_last_roll.total_seconds() < cooldown_seconds:
        remaining = cooldown_seconds - int(time_since_last_roll.total_seconds())
        minutes = remaining // 60
        seconds = remaining % 60
        return False, f"Please wait {minutes}m {seconds}s before rolling again."
    
    return True, ""


def can_claim_daily_bonus(user) -> tuple[bool, str]:
    """Check if user can claim daily bonus."""
    if not user.last_daily_bonus:
        return True, ""
    
    time_since_last_bonus = datetime.utcnow() - user.last_daily_bonus
    if time_since_last_bonus.total_seconds() < 86400:  # 24 hours
        remaining = 86400 - int(time_since_last_bonus.total_seconds())
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        return False, f"Daily bonus available in {hours}h {minutes}m"
    
    return True, ""


def get_referral_link(bot_username: str, user_id: int) -> str:
    """Generate referral link for user."""
    return f"https://t.me/{bot_username}?start={user_id}"


def extract_referrer_id(start_param: str) -> int:
    """Extract referrer ID from start parameter."""
    try:
        return int(start_param)
    except (ValueError, TypeError):
        return None


def format_user_profile(user) -> str:
    """Format user profile information."""
    profile = f"👤 <b>Profile</b>\n\n"
    profile += f"🆔 ID: <code>{user.user_id}</code>\n"
    profile += f"👤 Username: @{user.username or 'N/A'}\n"
    profile += f"📅 Joined: {format_datetime(user.join_date)}\n"
    profile += f"💰 Balance: {format_currency(user.balance)}\n"
    profile += f"💎 Total Earned: {format_currency(user.total_earned)}\n"
    profile += f"👥 Referrals: {user.referral_count}\n"
    profile += f"🎲 Daily Rolls: {user.daily_rolls_count}\n"
    
    return profile


def format_transaction(transaction) -> str:
    """Format transaction for display."""
    emoji_map = {
        "game": "🎲",
        "bonus": "🎁",
        "referral": "👥",
        "withdrawal": "💸"
    }
    
    emoji = emoji_map.get(transaction.transaction_type, "💰")
    amount_str = format_currency(transaction.amount)
    date_str = format_datetime(transaction.created_at)
    
    return f"{emoji} {amount_str} - {transaction.transaction_type.title()}\n📅 {date_str}"


def format_withdrawal_request(request) -> str:
    """Format withdrawal request for admin display."""
    status_emoji = {
        "pending": "⏳",
        "paid": "✅",
        "rejected": "❌"
    }
    
    emoji = status_emoji.get(request.status, "❓")
    amount_str = format_currency(request.amount)
    date_str = format_datetime(request.created_at)
    
    return f"{emoji} {amount_str} - {request.status.upper()}\n👤 User: {request.user_id}\n📅 {date_str}"