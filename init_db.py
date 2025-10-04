"""
Database initialization script.
Run this once to set up the database tables and default configuration.
"""
import asyncio
from database.db import db
from utils.logger import logger


async def init_database():
    """Initialize database tables and default configuration."""
    try:
        logger.info("Initializing database...")
        
        # Create all tables
        await db.create_tables()
        logger.info("✅ Database tables created successfully")
        
        # Initialize default configuration
        await db.init_default_config()
        logger.info("✅ Default configuration initialized")
        
        # Test database connection
        test_user = await db.get_user(1)
        logger.info("✅ Database connection test successful")
        
        logger.info("🎉 Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_database())