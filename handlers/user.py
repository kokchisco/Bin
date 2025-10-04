"""
User-related handlers for the Telegram bot.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import db
from utils.helpers import format_currency, format_user_profile, get_referral_link, is_admin
from utils.keyboards import get_main_keyboard, get_admin_keyboard, get_dice_keyboard
from utils.logger import logger

router = Router()


class WithdrawalStates(StatesGroup):
    waiting_for_amount = State()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """Handle /start command."""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Extract referrer ID from start parameter
    referrer_id = None
    if message.text and len(message.text.split()) > 1:
        start_param = message.text.split()[1]
        referrer_id = int(start_param) if start_param.isdigit() else None
    
    # Check if user exists
    user = await db.get_user(user_id)
    
    if not user:
        # Create new user
        user = await db.create_user(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referrer_id=referrer_id
        )
        
        # Handle referral bonus
        if referrer_id:
            referrer = await db.get_user(referrer_id)
            if referrer:
                referral_reward = await db.get_config("referral_reward", 50)
                await db.update_user_balance(
                    referrer_id, 
                    referral_reward, 
                    "referral", 
                    f"Referral bonus for {username or user_id}"
                )
                referrer.referral_count += 1
                await db.session_factory().commit()
                
                # Reward new user too
                await db.update_user_balance(
                    user_id, 
                    referral_reward, 
                    "referral", 
                    f"Welcome bonus from referral"
                )
        
        welcome_text = f"🎉 Welcome to the bot, {first_name}!\n\n"
        welcome_text += "You can earn rewards by playing games, claiming daily bonuses, and referring friends!\n\n"
        welcome_text += "Use the menu below to get started:"
        
        logger.info(f"New user registered: {user_id} (@{username})")
    else:
        welcome_text = f"👋 Welcome back, {first_name}!\n\n"
        welcome_text += "Use the menu below to continue earning:"
    
    # Send appropriate keyboard
    keyboard = get_admin_keyboard() if is_admin(user_id) else get_main_keyboard()
    
    await message.answer(welcome_text, reply_markup=keyboard)
    await state.clear()


@router.message(F.text == "👤 Profile")
async def profile_handler(message: Message):
    """Handle profile command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    profile_text = format_user_profile(user)
    await message.answer(profile_text, parse_mode="HTML")


@router.message(F.text == "💰 Balance")
async def balance_handler(message: Message):
    """Handle balance command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    currency_symbol = await db.get_config("currency_symbol", "₦")
    balance_text = f"💰 <b>Your Balance</b>\n\n"
    balance_text += f"Current Balance: {format_currency(user.balance, currency_symbol)}\n"
    balance_text += f"Total Earned: {format_currency(user.total_earned, currency_symbol)}\n"
    balance_text += f"Referrals: {user.referral_count}\n"
    
    await message.answer(balance_text, parse_mode="HTML")


@router.message(F.text == "👥 Referrals")
async def referrals_handler(message: Message):
    """Handle referrals command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    # Get bot username (you might want to store this in config)
    bot_username = "your_bot_username"  # Replace with actual bot username
    referral_link = get_referral_link(bot_username, user_id)
    
    referrals_text = f"👥 <b>Referral Program</b>\n\n"
    referrals_text += f"Your Referral Link:\n<code>{referral_link}</code>\n\n"
    referrals_text += f"Total Referrals: {user.referral_count}\n"
    referrals_text += f"Earned from Referrals: {format_currency(user.total_earned, await db.get_config('currency_symbol', '₦'))}\n\n"
    referrals_text += "Share your link to earn rewards when friends join!"
    
    await message.answer(referrals_text, parse_mode="HTML")


@router.message(F.text == "📜 Transactions")
async def transactions_handler(message: Message):
    """Handle transactions command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    transactions = await db.get_user_transactions(user_id, 10)
    
    if not transactions:
        await message.answer("📜 <b>Transaction History</b>\n\nNo transactions found.")
        return
    
    transactions_text = "📜 <b>Recent Transactions</b>\n\n"
    for transaction in transactions:
        currency_symbol = await db.get_config("currency_symbol", "₦")
        emoji_map = {
            "game": "🎲",
            "bonus": "🎁",
            "referral": "👥",
            "withdrawal": "💸"
        }
        
        emoji = emoji_map.get(transaction.transaction_type, "💰")
        amount_str = format_currency(transaction.amount, currency_symbol)
        date_str = transaction.created_at.strftime("%m-%d %H:%M")
        
        transactions_text += f"{emoji} {amount_str} - {transaction.transaction_type.title()}\n"
        transactions_text += f"📅 {date_str}\n\n"
    
    await message.answer(transactions_text, parse_mode="HTML")


@router.message(F.text == "ℹ️ Help")
async def help_handler(message: Message):
    """Handle help command."""
    help_text = "ℹ️ <b>Bot Help</b>\n\n"
    help_text += "🎲 <b>Play Game</b> - Roll dice to earn rewards\n"
    help_text += "💰 <b>Balance</b> - Check your current balance\n"
    help_text += "👤 <b>Profile</b> - View your profile information\n"
    help_text += "💸 <b>Withdraw</b> - Request withdrawal of your earnings\n"
    help_text += "📜 <b>Transactions</b> - View your transaction history\n"
    help_text += "👥 <b>Referrals</b> - Get your referral link and stats\n"
    help_text += "🎁 <b>Daily Bonus</b> - Claim your daily bonus\n\n"
    help_text += "For support, contact the admin."
    
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text == "🎲 Play Game")
async def play_game_handler(message: Message):
    """Handle play game command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    # Check cooldown
    cooldown = await db.get_config("dice_cooldown", 300)
    can_roll, message_text = can_roll_dice(user, cooldown)
    
    if not can_roll:
        await message.answer(f"⏳ {message_text}")
        return
    
    # Check daily roll limit
    max_rolls = await db.get_config("max_daily_rolls", 10)
    if user.daily_rolls_count >= max_rolls:
        await message.answer("🎲 You've reached your daily roll limit. Try again tomorrow!")
        return
    
    game_text = "🎲 <b>Dice Game</b>\n\n"
    game_text += "Click the button below to roll the dice and earn rewards!\n"
    game_text += f"Daily Rolls: {user.daily_rolls_count}/{max_rolls}\n\n"
    game_text += "Rewards:\n"
    game_text += "🎲 1 = 10 points\n"
    game_text += "🎲 2 = 20 points\n"
    game_text += "🎲 3 = 30 points\n"
    game_text += "🎲 4 = 40 points\n"
    game_text += "🎲 5 = 50 points\n"
    game_text += "🎲 6 = 100 points"
    
    await message.answer(game_text, reply_markup=get_dice_keyboard(), parse_mode="HTML")


@router.message(F.text == "🎁 Daily Bonus")
async def daily_bonus_handler(message: Message):
    """Handle daily bonus command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    # Check if user can claim daily bonus
    can_claim, message_text = can_claim_daily_bonus(user)
    
    if not can_claim:
        await message.answer(f"⏳ {message_text}")
        return
    
    # Give daily bonus
    bonus_amount = await db.get_config("daily_bonus", 100)
    await db.update_user_balance(
        user_id, 
        bonus_amount, 
        "bonus", 
        "Daily bonus"
    )
    
    # Update last daily bonus time
    from datetime import datetime
    user.last_daily_bonus = datetime.utcnow()
    await db.session_factory().commit()
    
    currency_symbol = await db.get_config("currency_symbol", "₦")
    bonus_text = f"🎁 <b>Daily Bonus Claimed!</b>\n\n"
    bonus_text += f"You received {format_currency(bonus_amount, currency_symbol)}!\n"
    bonus_text += f"New Balance: {format_currency(user.balance + bonus_amount, currency_symbol)}"
    
    await message.answer(bonus_text, parse_mode="HTML")
    logger.info(f"User {user_id} claimed daily bonus: {bonus_amount}")


@router.message(F.text == "💸 Withdraw")
async def withdraw_handler(message: Message, state: FSMContext):
    """Handle withdraw command."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ User not found. Please use /start to register.")
        return
    
    min_withdrawal = await db.get_config("min_withdrawal", 1000)
    currency_symbol = await db.get_config("currency_symbol", "₦")
    
    if user.balance < min_withdrawal:
        withdraw_text = f"💸 <b>Withdrawal</b>\n\n"
        withdraw_text += f"Minimum withdrawal: {format_currency(min_withdrawal, currency_symbol)}\n"
        withdraw_text += f"Your balance: {format_currency(user.balance, currency_symbol)}\n\n"
        withdraw_text += f"You need {format_currency(min_withdrawal - user.balance, currency_symbol)} more to withdraw."
        
        await message.answer(withdraw_text, parse_mode="HTML")
        return
    
    withdraw_text = f"💸 <b>Withdrawal Request</b>\n\n"
    withdraw_text += f"Your balance: {format_currency(user.balance, currency_symbol)}\n"
    withdraw_text += f"Minimum withdrawal: {format_currency(min_withdrawal, currency_symbol)}\n\n"
    withdraw_text += "Enter the amount you want to withdraw:"
    
    await message.answer(withdraw_text, parse_mode="HTML")
    await state.set_state(WithdrawalStates.waiting_for_amount)


@router.message(WithdrawalStates.waiting_for_amount)
async def process_withdrawal_amount(message: Message, state: FSMContext):
    """Process withdrawal amount input."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    try:
        amount = float(message.text)
        min_withdrawal = await db.get_config("min_withdrawal", 1000)
        currency_symbol = await db.get_config("currency_symbol", "₦")
        
        if amount < min_withdrawal:
            await message.answer(f"❌ Minimum withdrawal amount is {format_currency(min_withdrawal, currency_symbol)}")
            return
        
        if amount > user.balance:
            await message.answer(f"❌ Insufficient balance. Your balance: {format_currency(user.balance, currency_symbol)}")
            return
        
        # Create withdrawal request
        from database.models import WithdrawRequest
        async with db.session_factory() as session:
            withdraw_request = WithdrawRequest(
                user_id=user_id,
                amount=amount,
                status="pending"
            )
            session.add(withdraw_request)
            await session.commit()
            await session.refresh(withdraw_request)
        
        # Deduct from balance
        await db.update_user_balance(
            user_id, 
            -amount, 
            "withdrawal", 
            f"Withdrawal request #{withdraw_request.id}"
        )
        
        # Notify admin
        admin_id = await db.get_config("ADMIN_ID", 0)
        if admin_id:
            from aiogram import Bot
            bot = Bot.get_current()
            admin_text = f"🔔 <b>New Withdrawal Request</b>\n\n"
            admin_text += f"User: {user_id} (@{user.username or 'N/A'})\n"
            admin_text += f"Amount: {format_currency(amount, currency_symbol)}\n"
            admin_text += f"Request ID: {withdraw_request.id}"
            
            await bot.send_message(admin_id, admin_text, parse_mode="HTML")
        
        success_text = f"✅ <b>Withdrawal Request Submitted</b>\n\n"
        success_text += f"Amount: {format_currency(amount, currency_symbol)}\n"
        success_text += f"Request ID: {withdraw_request.id}\n\n"
        success_text += "Your request will be processed within 24 hours."
        
        await message.answer(success_text, parse_mode="HTML")
        await state.clear()
        
        logger.info(f"Withdrawal request created: User {user_id}, Amount {amount}")
        
    except ValueError:
        await message.answer("❌ Please enter a valid amount (numbers only)")
    except Exception as e:
        await message.answer("❌ An error occurred. Please try again.")
        logger.error(f"Withdrawal error: {e}")


# Import the can_roll_dice and can_claim_daily_bonus functions
from utils.helpers import can_roll_dice, can_claim_daily_bonus