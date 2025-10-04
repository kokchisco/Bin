"""
Keyboard layouts for the Telegram bot.
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(text="🎲 Play Game"), KeyboardButton(text="💰 Balance")],
            [KeyboardButton(text="👤 Profile"), KeyboardButton(text="💸 Withdraw")],
            [KeyboardButton(text="📜 Transactions"), KeyboardButton(text="👥 Referrals")],
            [KeyboardButton(text="🎁 Daily Bonus"), KeyboardButton(text="ℹ️ Help")]
        ]
    )
    return keyboard


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Get admin keyboard (includes main keyboard + admin buttons)."""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(text="🎲 Play Game"), KeyboardButton(text="💰 Balance")],
            [KeyboardButton(text="👤 Profile"), KeyboardButton(text="💸 Withdraw")],
            [KeyboardButton(text="📜 Transactions"), KeyboardButton(text="👥 Referrals")],
            [KeyboardButton(text="🎁 Daily Bonus"), KeyboardButton(text="ℹ️ Help")],
            [KeyboardButton(text="⚙️ Admin Panel")]
        ]
    )
    return keyboard


def get_dice_keyboard() -> InlineKeyboardMarkup:
    """Get dice game keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Roll Dice", callback_data="roll_dice")]
        ]
    )
    return keyboard


def get_withdrawal_keyboard() -> InlineKeyboardMarkup:
    """Get withdrawal confirmation keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_withdrawal"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_withdrawal")
            ]
        ]
    )
    return keyboard


def get_admin_withdrawal_keyboard(request_id: int) -> InlineKeyboardMarkup:
    """Get admin withdrawal management keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Approve", callback_data=f"approve_withdrawal_{request_id}"),
                InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_withdrawal_{request_id}")
            ]
        ]
    )
    return keyboard


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Get admin panel keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 All Users", callback_data="admin_all_users")],
            [InlineKeyboardButton(text="💸 Pending Withdrawals", callback_data="admin_pending_withdrawals")],
            [InlineKeyboardButton(text="⚙️ Settings", callback_data="admin_settings")],
            [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="📊 Statistics", callback_data="admin_stats")]
        ]
    )
    return keyboard


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Get settings management keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💰 Min Withdrawal", callback_data="setting_min_withdrawal")],
            [InlineKeyboardButton(text="🎁 Daily Bonus", callback_data="setting_daily_bonus")],
            [InlineKeyboardButton(text="👥 Referral Reward", callback_data="setting_referral_reward")],
            [InlineKeyboardButton(text="💱 Currency Symbol", callback_data="setting_currency")],
            [InlineKeyboardButton(text="⏱️ Dice Cooldown", callback_data="setting_dice_cooldown")],
            [InlineKeyboardButton(text="🔙 Back to Admin", callback_data="admin_panel")]
        ]
    )
    return keyboard


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Get cancel operation keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_operation")]
        ]
    )
    return keyboard