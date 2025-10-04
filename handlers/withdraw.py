"""
Withdrawal-related handlers for the Telegram bot.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.db import db
from utils.helpers import is_admin, format_currency, format_withdrawal_request
from utils.keyboards import get_admin_withdrawal_keyboard, get_cancel_keyboard
from utils.logger import logger

router = Router()


@router.callback_query(F.data.startswith("approve_withdrawal_"))
async def approve_withdrawal_callback(callback: CallbackQuery):
    """Handle approve withdrawal callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    request_id = int(callback.data.replace("approve_withdrawal_", ""))
    
    try:
        # Get withdrawal request
        async with db.session_factory() as session:
            from database.models import WithdrawRequest
            from sqlalchemy import select
            
            stmt = select(WithdrawRequest).where(WithdrawRequest.id == request_id)
            result = await session.execute(stmt)
            withdraw_request = result.scalar_one_or_none()
            
            if not withdraw_request:
                await callback.answer("❌ Withdrawal request not found.")
                return
            
            if withdraw_request.status != "pending":
                await callback.answer("❌ This withdrawal request has already been processed.")
                return
            
            # Update status
            withdraw_request.status = "paid"
            from datetime import datetime
            withdraw_request.processed_at = datetime.utcnow()
            await session.commit()
        
        # Notify user
        from aiogram import Bot
        bot = Bot.get_current()
        
        currency_symbol = await db.get_config("currency_symbol", "₦")
        user_text = f"✅ <b>Withdrawal Approved</b>\n\n"
        user_text += f"Request ID: {request_id}\n"
        user_text += f"Amount: {format_currency(withdraw_request.amount, currency_symbol)}\n\n"
        user_text += "Your withdrawal has been processed successfully!"
        
        try:
            await bot.send_message(withdraw_request.user_id, user_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to notify user {withdraw_request.user_id} of withdrawal approval: {e}")
        
        # Update admin message
        admin_text = f"✅ <b>Withdrawal Approved</b>\n\n"
        admin_text += f"Request ID: {request_id}\n"
        admin_text += f"User: {withdraw_request.user_id}\n"
        admin_text += f"Amount: {format_currency(withdraw_request.amount, currency_symbol)}\n"
        admin_text += f"Status: PAID"
        
        await callback.message.edit_text(admin_text, parse_mode="HTML")
        await callback.answer("✅ Withdrawal approved and user notified.")
        
        logger.info(f"Admin {user_id} approved withdrawal request {request_id}")
        
    except Exception as e:
        await callback.answer("❌ An error occurred. Please try again.")
        logger.error(f"Withdrawal approval error: {e}")


@router.callback_query(F.data.startswith("reject_withdrawal_"))
async def reject_withdrawal_callback(callback: CallbackQuery):
    """Handle reject withdrawal callback."""
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("❌ Access denied. Admin only.")
        return
    
    request_id = int(callback.data.replace("reject_withdrawal_", ""))
    
    try:
        # Get withdrawal request
        async with db.session_factory() as session:
            from database.models import WithdrawRequest
            from sqlalchemy import select
            
            stmt = select(WithdrawRequest).where(WithdrawRequest.id == request_id)
            result = await session.execute(stmt)
            withdraw_request = result.scalar_one_or_none()
            
            if not withdraw_request:
                await callback.answer("❌ Withdrawal request not found.")
                return
            
            if withdraw_request.status != "pending":
                await callback.answer("❌ This withdrawal request has already been processed.")
                return
            
            # Update status
            withdraw_request.status = "rejected"
            from datetime import datetime
            withdraw_request.processed_at = datetime.utcnow()
            await session.commit()
            
            # Refund the amount to user balance
            await db.update_user_balance(
                withdraw_request.user_id,
                withdraw_request.amount,
                "withdrawal_refund",
                f"Withdrawal request #{request_id} rejected - refunded"
            )
        
        # Notify user
        from aiogram import Bot
        bot = Bot.get_current()
        
        currency_symbol = await db.get_config("currency_symbol", "₦")
        user_text = f"❌ <b>Withdrawal Rejected</b>\n\n"
        user_text += f"Request ID: {request_id}\n"
        user_text += f"Amount: {format_currency(withdraw_request.amount, currency_symbol)}\n\n"
        user_text += "Your withdrawal request has been rejected. The amount has been refunded to your balance."
        
        try:
            await bot.send_message(withdraw_request.user_id, user_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to notify user {withdraw_request.user_id} of withdrawal rejection: {e}")
        
        # Update admin message
        admin_text = f"❌ <b>Withdrawal Rejected</b>\n\n"
        admin_text += f"Request ID: {request_id}\n"
        admin_text += f"User: {withdraw_request.user_id}\n"
        admin_text += f"Amount: {format_currency(withdraw_request.amount, currency_symbol)}\n"
        admin_text += f"Status: REJECTED (Refunded)"
        
        await callback.message.edit_text(admin_text, parse_mode="HTML")
        await callback.answer("❌ Withdrawal rejected and user notified.")
        
        logger.info(f"Admin {user_id} rejected withdrawal request {request_id}")
        
    except Exception as e:
        await callback.answer("❌ An error occurred. Please try again.")
        logger.error(f"Withdrawal rejection error: {e}")


@router.callback_query(F.data == "cancel_operation")
async def cancel_operation_callback(callback: CallbackQuery):
    """Handle cancel operation callback."""
    await callback.message.edit_text("❌ Operation cancelled.")
    await callback.answer()