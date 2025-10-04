"""
Database models for the Telegram bot.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model for storing user information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    balance = Column(Float, default=0.0)
    total_earned = Column(Float, default=0.0)
    referral_count = Column(Integer, default=0)
    referrer_id = Column(Integer, nullable=True)
    join_date = Column(DateTime, default=datetime.utcnow)
    last_dice_roll = Column(DateTime, nullable=True)
    last_daily_bonus = Column(DateTime, nullable=True)
    daily_rolls_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    game_history = relationship("GameHistory", back_populates="user")
    withdraw_requests = relationship("WithdrawRequest", back_populates="user")


class Transaction(Base):
    """Transaction model for tracking all balance changes."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # game, bonus, referral, withdrawal
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")


class GameHistory(Base):
    """Game history model for tracking game plays."""
    __tablename__ = "game_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    game_type = Column(String(50), default="dice")
    dice_value = Column(Integer, nullable=True)
    reward = Column(Float, nullable=False)
    played_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="game_history")


class WithdrawRequest(Base):
    """Withdrawal request model."""
    __tablename__ = "withdraw_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, paid, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    admin_notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="withdraw_requests")


class Config(Base):
    """Configuration model for dynamic settings."""
    __tablename__ = "config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)