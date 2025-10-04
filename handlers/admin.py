"""
Admin-related handlers for the Telegram bot.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import db
from utils.helpers import is_admin, format_currency, format_user_profile, format_withdrawal_request
from utils.keyboards import get_admin_panel_keyboard, get_settings_keyboard, get_cancel_keyboard
from utils.logger import logger

router = Router()


class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_setting_value = State()


@router.message(F.text == "⚙️ Admin Panel")
async def admin_panel_handler(message: Message):
    """Handle admin panel command."""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ Access denied. Admin only.")
        return
    
    admin_text = "⚙️ <b>Admin Panel</b>\n\n"
    admin_text += "Select an option below:"
    
    await message.answer(admin_text, reply_markup=get_admin_panel_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery):
    """Handle admin panel callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    admin_text = "⚙️ <b>Admin Panel</b>\n\n"
    admin_text += "Select an option below:"
    
    await callback.message.edit_text(admin_text, reply_markup=get_admin_panel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_all_users")
async def admin_all_users_callback(callback: CallbackQuery):
    """Handle admin all users callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    users = await db.get_all_users(50)
    
    if not users:
        await callback.message.edit_text("👥 <b>All Users</b>\n\nNo users found.")
        return
    
    users_text = "👥 <b>All Users</b>\n\n"
    for user in users[:20]:  # Show first 20 users
        users_text += f"👤 {user.user_id} (@{user.username or 'N/A'})\n"
        users_text += f"💰 {format_currency(user.balance)}\n"
        users_text += f"📅 {user.join_date.strftime('%Y-%m-%d')}\n\n"
    
    if len(users) > 20:
        users_text += f"... and {len(users) - 20} more users"
    
    await callback.message.edit_text(users_text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_pending_withdrawals")
async def admin_pending_withdrawals_callback(callback: CallbackQuery):
    """Handle admin pending withdrawals callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    withdrawals = await db.get_pending_withdrawals()
    
    if not withdrawals:
        await callback.message.edit_text("💸 <b>Pending Withdrawals</b>\n\nNo pending withdrawals found.")
        return
    
    withdrawals_text = "💸 <b>Pending Withdrawals</b>\n\n"
    for withdrawal in withdrawals[:10]:  # Show first 10
        withdrawals_text += f"🆔 Request #{withdrawal.id}\n"
        withdrawals_text += f"👤 User: {withdrawal.user_id}\n"
        withdrawals_text += f"💰 Amount: {format_currency(withdrawal.amount)}\n"
        withdrawals_text += f"📅 Date: {withdrawal.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
    
    await callback.message.edit_text(withdrawals_text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_settings")
async def admin_settings_callback(callback: CallbackQuery):
    """Handle admin settings callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    # Get current settings
    currency_symbol = await db.get_config("currency_symbol", "₦")
    min_withdrawal = await db.get_config("min_withdrawal", 1000)
    daily_bonus = await db.get_config("daily_bonus", 100)
    referral_reward = await db.get_config("referral_reward", 50)
    dice_cooldown = await db.get_config("dice_cooldown", 300)
    
    settings_text = "⚙️ <b>Current Settings</b>\n\n"
    settings_text += f"💱 Currency: {currency_symbol}\n"
    settings_text += f"💰 Min Withdrawal: {format_currency(min_withdrawal, currency_symbol)}\n"
    settings_text += f"🎁 Daily Bonus: {format_currency(daily_bonus, currency_symbol)}\n"
    settings_text += f"👥 Referral Reward: {format_currency(referral_reward, currency_symbol)}\n"
    settings_text += f"⏱️ Dice Cooldown: {dice_cooldown // 60} minutes\n\n"
    settings_text += "Select a setting to modify:"
    
    await callback.message.edit_text(settings_text, reply_markup=get_settings_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("setting_"))
async def admin_setting_callback(callback: CallbackQuery, state: FSMContext):
    """Handle admin setting modification callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    setting_type = callback.data.replace("setting_", "")
    
    # Store setting type in state
    await state.update_data(setting_type=setting_type)
    
    setting_prompts = {
        "min_withdrawal": "Enter new minimum withdrawal amount:",
        "daily_bonus": "Enter new daily bonus amount:",
        "referral_reward": "Enter new referral reward amount:",
        "currency": "Enter new currency symbol:",
        "dice_cooldown": "Enter new dice cooldown in minutes:"
    }
    
    prompt = setting_prompts.get(setting_type, "Enter new value:")
    
    await callback.message.edit_text(f"⚙️ <b>Modify Setting</b>\n\n{prompt}", reply_markup=get_cancel_keyboard(), parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_setting_value)
    await callback.answer()


@router.message(AdminStates.waiting_for_setting_value)
async def process_setting_value(message: Message, state: FSMContext):
    """Process setting value input."""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ Access denied. Admin only.")
        return
    
    data = await state.get_data()
    setting_type = data.get("setting_type")
    
    try:
        if setting_type == "currency":
            # Currency symbol doesn't need conversion
            value = message.text.strip()
            await db.set_config("currency_symbol", value)
            await message.answer(f"✅ Currency symbol updated to: {value}")
            
        elif setting_type == "dice_cooldown":
            # Convert minutes to seconds
            minutes = int(message.text)
            seconds = minutes * 60
            await db.set_config("dice_cooldown", seconds)
            await message.answer(f"✅ Dice cooldown updated to: {minutes} minutes")
            
        else:
            # Numeric values
            value = float(message.text)
            config_key = setting_type
            await db.set_config(config_key, value)
            await message.answer(f"✅ {setting_type.replace('_', ' ').title()} updated to: {value}")
        
        await state.clear()
        logger.info(f"Admin {user_id} updated setting {setting_type} to {message.text}")
        
    except ValueError:
        await message.answer("❌ Please enter a valid value.")
    except Exception as e:
        await message.answer("❌ An error occurred. Please try again.")
        logger.error(f"Admin setting update error: {e}")


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_callback(callback: CallbackQuery, state: FSMContext):
    """Handle admin broadcast callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    await callback.message.edit_text("📢 <b>Broadcast Message</b>\n\nEnter the message you want to broadcast to all users:", reply_markup=get_cancel_keyboard(), parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast_message(message: Message, state: FSMContext):
    """Process broadcast message."""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ Access denied. Admin only.")
        return
    
    broadcast_text = message.text
    
    # Get all users
    users = await db.get_all_users()
    
    # Send to all users
    from aiogram import Bot
    bot = Bot.get_current()
    
    sent_count = 0
    failed_count = 0
    
    for user in users:
        try:
            await bot.send_message(user.user_id, f"📢 <b>Broadcast Message</b>\n\n{broadcast_text}", parse_mode="HTML")
            sent_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to send broadcast to user {user.user_id}: {e}")
    
    result_text = f"📢 <b>Broadcast Complete</b>\n\n"
    result_text += f"✅ Sent: {sent_count}\n"
    result_text += f"❌ Failed: {failed_count}\n"
    result_text += f"📊 Total: {len(users)}"
    
    await message.answer(result_text, parse_mode="HTML")
    await state.clear()
    
    logger.info(f"Admin {user_id} sent broadcast to {sent_count} users")


@router.callback_query(F.data == "admin_stats")
async def admin_stats_callback(callback: CallbackQuery):
    """Handle admin stats callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    # Get statistics
    users = await db.get_all_users()
    total_users = len(users)
    
    # Calculate total balance
    total_balance = sum(user.balance for user in users)
    total_earned = sum(user.total_earned for user in users)
    
    # Get pending withdrawals
    withdrawals = await db.get_pending_withdrawals()
    pending_withdrawals = len(withdrawals)
    pending_amount = sum(w.amount for w in withdrawals)
    
    stats_text = "📊 <b>Bot Statistics</b>\n\n"
    stats_text += f"👥 Total Users: {total_users}\n"
    stats_text += f"💰 Total Balance: {format_currency(total_balance)}\n"
    stats_text += f"💎 Total Earned: {format_currency(total_earned)}\n"
    stats_text += f"⏳ Pending Withdrawals: {pending_withdrawals}\n"
    stats_text += f"💸 Pending Amount: {format_currency(pending_amount)}\n"
    
    await callback.message.edit_text(stats_text, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "cancel_operation")
async def cancel_operation_callback(callback: CallbackQuery, state: FSMContext):
    """Handle cancel operation callback."""
    await state.clear()
    await callback.message.edit_text("❌ Operation cancelled.")
    await callback.answer()