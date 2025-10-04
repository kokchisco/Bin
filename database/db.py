"""
Database connection and session management.
"""
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, DEFAULT_CONFIG
from .models import Base, User, Config

# Create async engine
engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,
    future=True
)

# Create async session factory
async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


class Database:
    """Database manager class."""
    
    def __init__(self):
        self.engine = engine
        self.session_factory = async_session
    
    async def create_tables(self):
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def init_default_config(self):
        """Initialize default configuration values."""
        async with self.session_factory() as session:
            for key, value in DEFAULT_CONFIG.items():
                # Check if config already exists
                existing = await session.get(Config, key)
                if not existing:
                    config = Config(key=key, value=str(value))
                    session.add(config)
            await session.commit()
    
    async def get_config(self, key: str, default_value=None):
        """Get configuration value."""
        async with self.session_factory() as session:
            config = await session.get(Config, key)
            if config:
                # Try to convert to appropriate type
                value = config.value
                if isinstance(default_value, int):
                    return int(value)
                elif isinstance(default_value, float):
                    return float(value)
                elif isinstance(default_value, bool):
                    return value.lower() in ('true', '1', 'yes', 'on')
                return value
            return default_value
    
    async def set_config(self, key: str, value):
        """Set configuration value."""
        async with self.session_factory() as session:
            config = await session.get(Config, key)
            if config:
                config.value = str(value)
            else:
                config = Config(key=key, value=str(value))
                session.add(config)
            await session.commit()
    
    async def get_user(self, user_id: int) -> User:
        """Get user by user_id."""
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            return user
    
    async def create_user(self, user_id: int, username: str = None, 
                         first_name: str = None, last_name: str = None, 
                         referrer_id: int = None) -> User:
        """Create a new user."""
        async with self.session_factory() as session:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                referrer_id=referrer_id
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def update_user_balance(self, user_id: int, amount: float, 
                                 transaction_type: str, description: str = None):
        """Update user balance and create transaction record."""
        async with self.session_factory() as session:
            user = await session.get(User, user_id)
            if user:
                user.balance += amount
                if amount > 0:
                    user.total_earned += amount
                
                # Create transaction record
                transaction = Transaction(
                    user_id=user_id,
                    transaction_type=transaction_type,
                    amount=amount,
                    description=description
                )
                session.add(transaction)
                await session.commit()
                return True
            return False
    
    async def get_user_transactions(self, user_id: int, limit: int = 10):
        """Get user's recent transactions."""
        async with self.session_factory() as session:
            from sqlalchemy import select
            from .models import Transaction
            
            stmt = select(Transaction).where(
                Transaction.user_id == user_id
            ).order_by(Transaction.created_at.desc()).limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
    
    async def get_pending_withdrawals(self):
        """Get all pending withdrawal requests."""
        async with self.session_factory() as session:
            from sqlalchemy import select
            from .models import WithdrawRequest
            
            stmt = select(WithdrawRequest).where(
                WithdrawRequest.status == "pending"
            ).order_by(WithdrawRequest.created_at.desc())
            
            result = await session.execute(stmt)
            return result.scalars().all()
    
    async def get_all_users(self, limit: int = 100):
        """Get all users (for admin)."""
        async with self.session_factory() as session:
            from sqlalchemy import select
            
            stmt = select(User).order_by(User.join_date.desc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()


# Global database instance
db = Database()