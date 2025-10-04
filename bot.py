"""
Main bot file for the Telegram bot.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, ADMIN_ID
from database.db import db
from handlers import register_user_handlers, register_admin_handlers, register_game_handlers, register_withdrawal_handlers
from utils.logger import logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register handlers
register_user_handlers(dp)
register_admin_handlers(dp)
register_game_handlers(dp)
register_withdrawal_handlers(dp)


async def on_startup():
    """Bot startup handler."""
    logger.info("Starting bot...")
    
    # Create database tables
    await db.create_tables()
    logger.info("Database tables created/verified")
    
    # Initialize default configuration
    await db.init_default_config()
    logger.info("Default configuration initialized")
    
    # Set bot commands
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help information"),
    ]
    await bot.set_my_commands(commands)
    
    logger.info("Bot started successfully!")


async def on_shutdown():
    """Bot shutdown handler."""
    logger.info("Shutting down bot...")
    await bot.session.close()
    logger.info("Bot shutdown complete")


async def main():
    """Main function."""
    try:
        # Register startup and shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Start polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")