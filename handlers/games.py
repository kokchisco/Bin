"""
Game-related handlers for the Telegram bot.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database.db import db
from utils.helpers import format_currency, can_roll_dice
from utils.keyboards import get_dice_keyboard
from utils.logger import logger
import random
from datetime import datetime

router = Router()


@router.callback_query(F.data == "roll_dice")
async def roll_dice_callback(callback: CallbackQuery, state: FSMContext):
    """Handle dice roll callback."""
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await callback.answer("❌ User not found. Please use /start to register.")
        return
    
    # Check cooldown
    cooldown = await db.get_config("dice_cooldown", 300)
    can_roll, message_text = can_roll_dice(user, cooldown)
    
    if not can_roll:
        await callback.answer(f"⏳ {message_text}")
        return
    
    # Check daily roll limit
    max_rolls = await db.get_config("max_daily_rolls", 10)
    if user.daily_rolls_count >= max_rolls:
        await callback.answer("🎲 You've reached your daily roll limit. Try again tomorrow!")
        return
    
    # Roll dice
    dice_value = random.randint(1, 6)
    reward = dice_value * 10  # Basic reward calculation
    
    # Update user balance
    await db.update_user_balance(
        user_id, 
        reward, 
        "game", 
        f"Dice roll: {dice_value}"
    )
    
    # Update user stats
    user.last_dice_roll = datetime.utcnow()
    user.daily_rolls_count += 1
    await db.session_factory().commit()
    
    # Create game history record
    from database.models import GameHistory
    async with db.session_factory() as session:
        game_record = GameHistory(
            user_id=user_id,
            game_type="dice",
            dice_value=dice_value,
            reward=reward
        )
        session.add(game_record)
        await session.commit()
    
    # Send result
    currency_symbol = await db.get_config("currency_symbol", "₦")
    result_text = f"🎲 <b>Dice Roll Result</b>\n\n"
    result_text += f"🎲 You rolled: <b>{dice_value}</b>\n"
    result_text += f"💰 Reward: {format_currency(reward, currency_symbol)}\n"
    result_text += f"💎 New Balance: {format_currency(user.balance + reward, currency_symbol)}\n\n"
    result_text += f"Daily Rolls: {user.daily_rolls_count}/{max_rolls}"
    
    # Check if user can roll again
    can_roll_again, _ = can_roll_dice(user, cooldown)
    if can_roll_again and user.daily_rolls_count < max_rolls:
        result_text += "\n\nClick the button below to roll again!"
        await callback.message.edit_text(result_text, reply_markup=get_dice_keyboard(), parse_mode="HTML")
    else:
        if user.daily_rolls_count >= max_rolls:
            result_text += "\n\n🎯 You've reached your daily roll limit!"
        else:
            result_text += f"\n\n⏳ Next roll available in {cooldown // 60} minutes"
        await callback.message.edit_text(result_text, parse_mode="HTML")
    
    await callback.answer()
    logger.info(f"User {user_id} rolled dice: {dice_value}, reward: {reward}")


@router.callback_query(F.data == "cancel_operation")
async def cancel_operation_callback(callback: CallbackQuery, state: FSMContext):
    """Handle cancel operation callback."""
    await state.clear()
    await callback.message.edit_text("❌ Operation cancelled.")
    await callback.answer()