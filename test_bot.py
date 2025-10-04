"""
Simple test script to verify bot functionality.
"""
import asyncio
from database.db import db
from utils.logger import logger


async def test_database_operations():
    """Test basic database operations."""
    try:
        logger.info("Testing database operations...")
        
        # Test creating a user
        test_user = await db.create_user(
            user_id=12345,
            username="test_user",
            first_name="Test",
            last_name="User"
        )
        logger.info(f"✅ Created test user: {test_user.user_id}")
        
        # Test updating balance
        await db.update_user_balance(
            test_user.user_id,
            100.0,
            "test",
            "Test transaction"
        )
        logger.info("✅ Updated user balance")
        
        # Test getting user
        retrieved_user = await db.get_user(test_user.user_id)
        logger.info(f"✅ Retrieved user: {retrieved_user.balance}")
        
        # Test getting transactions
        transactions = await db.get_user_transactions(test_user.user_id, 5)
        logger.info(f"✅ Retrieved {len(transactions)} transactions")
        
        # Test configuration
        currency = await db.get_config("currency_symbol", "₦")
        logger.info(f"✅ Retrieved config: {currency}")
        
        logger.info("🎉 All database operations test passed!")
        
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        raise


async def main():
    """Main test function."""
    try:
        await test_database_operations()
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Tests failed!")