# Telegram Bot - Rewards & Games System

A comprehensive Telegram bot built with Python, aiogram, and PostgreSQL that allows users to earn rewards through games, daily bonuses, and referrals. The bot is designed for high traffic and can be deployed on Render.

## 🚀 Features

### User Features
- **🎲 Dice Game**: Roll dice daily to earn random rewards (1-6 dice values with different point rewards)
- **💰 Balance System**: Track earnings and current balance with transaction history
- **👤 Profile Management**: View user stats, join date, and referral information
- **💸 Withdrawal System**: Request withdrawals when reaching minimum threshold
- **📜 Transaction History**: View all balance-affecting activities
- **👥 Referral Program**: Earn rewards by inviting friends with unique referral links
- **🎁 Daily Bonus**: Claim daily bonuses every 24 hours
- **⏱️ Rate Limiting**: Prevents spam with cooldown periods

### Admin Features
- **⚙️ Admin Panel**: Complete admin dashboard with user management
- **👥 User Management**: View all users and their statistics
- **💸 Withdrawal Management**: Approve/reject withdrawal requests
- **⚙️ Settings Management**: Configure bot parameters dynamically
- **📢 Broadcast System**: Send messages to all users
- **📊 Statistics**: View bot usage and financial statistics

## 🛠️ Tech Stack

- **Python 3.11+**
- **aiogram 3.4.1** - Modern async Telegram Bot API framework
- **asyncpg 0.29.0** - Fast PostgreSQL async driver
- **SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Primary database
- **Render** - Cloud hosting platform

## 📁 Project Structure

```
project/
├── bot.py                 # Main bot file
├── config.py             # Configuration and environment variables
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment configuration
├── .env                 # Environment variables (not in repo)
├── database/
│   ├── __init__.py
│   ├── models.py        # Database models
│   └── db.py           # Database connection and operations
├── handlers/
│   ├── __init__.py
│   ├── user.py         # User-related handlers
│   ├── admin.py        # Admin panel handlers
│   ├── games.py        # Game mechanics handlers
│   └── withdraw.py     # Withdrawal management handlers
└── utils/
    ├── __init__.py
    ├── helpers.py      # Helper functions
    ├── keyboards.py    # Keyboard layouts
    └── logger.py       # Logging configuration
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd telegram-bot
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file with the following variables:

```env
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://username:password@localhost:5432/telegram_bot
ADMIN_ID=your_admin_telegram_id
```

### 3. Database Setup

The bot will automatically create all necessary tables on first run. For manual setup:

```python
# Run this once to initialize the database
from database.db import db
import asyncio

async def init_db():
    await db.create_tables()
    await db.init_default_config()

asyncio.run(init_db())
```

### 4. Run Locally

```bash
python bot.py
```

## 🚀 Deployment on Render

### 1. Prepare for Deployment

1. **Update bot username**: In `handlers/user.py`, replace `"your_bot_username"` with your actual bot username
2. **Set environment variables** in Render dashboard:
   - `BOT_TOKEN`: Your bot token from @BotFather
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ADMIN_ID`: Your Telegram user ID

### 2. Deploy to Render

1. Connect your GitHub repository to Render
2. Create a new **Web Service**
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Environment**: Python 3.11

### 3. Database Setup

1. Create a PostgreSQL database on Render
2. Copy the database URL to your environment variables
3. The bot will automatically create tables on first run

## 🎮 Bot Commands

### User Commands
- `/start` - Start the bot and register
- `/help` - Show help information

### Menu Buttons
- **🎲 Play Game** - Roll dice to earn rewards
- **💰 Balance** - Check current balance
- **👤 Profile** - View profile information
- **💸 Withdraw** - Request withdrawal
- **📜 Transactions** - View transaction history
- **👥 Referrals** - Get referral link and stats
- **🎁 Daily Bonus** - Claim daily bonus
- **ℹ️ Help** - Show help information

### Admin Commands
- **⚙️ Admin Panel** - Access admin dashboard (admin only)

## ⚙️ Configuration

The bot uses a dynamic configuration system stored in the database. Admins can modify these settings:

- **Currency Symbol**: Default "₦" (Naira)
- **Minimum Withdrawal**: Default 1000
- **Daily Bonus**: Default 100
- **Referral Reward**: Default 50
- **Dice Cooldown**: Default 5 minutes
- **Max Daily Rolls**: Default 10

## 🎲 Game Mechanics

### Dice Game
- Roll dice (1-6) to earn rewards
- Rewards: dice_value × 10 points
- Cooldown: 5 minutes between rolls
- Daily limit: 10 rolls per day
- Special reward for rolling 6: 100 points

### Daily Bonus
- Claim once every 24 hours
- Fixed amount (configurable by admin)
- Resets at midnight UTC

### Referral System
- Each user gets unique referral link
- Both referrer and referee get rewards
- Rewards are configurable by admin

## 💰 Withdrawal System

1. Users can request withdrawal when balance ≥ minimum
2. Admin receives notification of new requests
3. Admin can approve or reject requests
4. Rejected requests refund the amount to user balance
5. All actions are logged and tracked

## 🔒 Security Features

- **Rate Limiting**: Prevents spam and abuse
- **Admin-only Commands**: Protected admin functions
- **Input Validation**: All user inputs are validated
- **Error Handling**: Comprehensive error handling
- **Logging**: All actions are logged for audit

## 📊 Database Schema

### Users Table
- User information, balance, referral stats
- Tracks join date, last activity, daily limits

### Transactions Table
- All balance-affecting activities
- Transaction type, amount, description, timestamp

### Game History Table
- Game play records
- Dice values, rewards, timestamps

### Withdraw Requests Table
- Withdrawal request management
- Status tracking, admin notes

### Config Table
- Dynamic configuration storage
- Key-value pairs for bot settings

## 🚀 Scaling Considerations

The bot is designed for high traffic with:

- **Async Operations**: All database operations are async
- **Connection Pooling**: Efficient database connection management
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Modular Design**: Easy to add new features
- **Error Recovery**: Graceful error handling and recovery

## 🛠️ Development

### Adding New Games

1. Create new game handler in `handlers/games.py`
2. Add game logic and reward calculation
3. Update user interface and keyboards
4. Add game history tracking

### Adding New Features

1. Create new handler module in `handlers/`
2. Register handlers in `handlers/__init__.py`
3. Update keyboards in `utils/keyboards.py`
4. Add database models if needed

## 📝 Logging

The bot includes comprehensive logging:

- **File Logging**: Daily log files
- **Console Logging**: Error-level messages
- **Action Logging**: All user and admin actions
- **Error Tracking**: Detailed error information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support or questions:
1. Check the logs for error messages
2. Verify environment variables are set correctly
3. Ensure database connection is working
4. Contact the admin through the bot

## 🔄 Updates

The bot supports dynamic configuration updates without restart:
- Admin can modify settings through the admin panel
- Changes take effect immediately
- No downtime required for configuration changes

---

**Built with ❤️ using Python, aiogram, and PostgreSQL**