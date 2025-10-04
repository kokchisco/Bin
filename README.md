# 🎲 Telegram Dice Bot

A comprehensive Telegram bot built with Python, aiogram, and PostgreSQL for high-traffic gaming and reward systems. Users can play dice games, earn rewards, manage withdrawals, and participate in a referral program.

## 🚀 Features

### 🎮 Gaming System
- **Dice Rolling**: Roll dice to earn random rewards (1-6 with different payout multipliers)
- **Daily Limits**: Configurable daily roll limits to prevent abuse
- **Cooldown System**: Rate limiting to prevent spam
- **Game History**: Track all game plays and rewards

### 💰 Reward System
- **Balance Management**: Real-time balance tracking with PostgreSQL
- **Transaction History**: Complete audit trail of all balance changes
- **Daily Bonuses**: Claim daily rewards (24-hour cooldown)
- **Referral Program**: Earn rewards for inviting friends

### 💸 Withdrawal System
- **Minimum Threshold**: Configurable minimum withdrawal amounts
- **Admin Approval**: All withdrawals require admin approval
- **Status Tracking**: Pending, approved, or rejected status
- **Automatic Refunds**: Rejected withdrawals are automatically refunded

### 👥 User Management
- **Auto Registration**: Users are automatically created on first interaction
- **Profile System**: View user stats, balance, and transaction history
- **Referral Links**: Unique referral links for each user
- **Admin Panel**: Comprehensive admin controls

### ⚙️ Admin Features
- **User Management**: View all users and their statistics
- **Withdrawal Management**: Approve or reject withdrawal requests
- **Configuration**: Dynamic settings management
- **Broadcasting**: Send messages to all users
- **Statistics**: Real-time bot usage statistics

## 🛠️ Tech Stack

- **Python 3.11+**
- **aiogram 3.4.1** - Modern async Telegram Bot API framework
- **asyncpg 0.29.0** - Fast PostgreSQL async driver
- **SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Primary database
- **Render** - Cloud hosting platform

## 📁 Project Structure

```
telegram-bot/
│
├── bot.py                 # Main bot entry point
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment configuration
├── .env                  # Environment variables (not in git)
│
├── database/
│   ├── __init__.py
│   ├── models.py         # SQLAlchemy database models
│   └── db.py            # Database connection and operations
│
├── handlers/
│   ├── __init__.py
│   ├── user.py          # User-related handlers
│   ├── admin.py         # Admin panel handlers
│   ├── games.py         # Game mechanics handlers
│   └── withdraw.py      # Withdrawal system handlers
│
└── utils/
    ├── __init__.py
    ├── helpers.py       # Utility functions
    ├── keyboards.py     # Telegram keyboard layouts
    └── logger.py        # Logging configuration
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Telegram Bot Token (from @BotFather)

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd telegram-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. **Create a `.env` file** in the project root:
```env
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://username:password@localhost:5432/telegram_bot
ADMIN_ID=your_telegram_user_id
```

2. **Set up PostgreSQL database**:
```sql
CREATE DATABASE telegram_bot;
```

### 4. Database Initialization

The bot will automatically create all necessary tables and initialize default configuration on first run. No manual migration is required.

### 5. Run the Bot

```bash
python bot.py
```

## 🚀 Deployment on Render

### 1. Prepare for Deployment

1. **Update `requirements.txt`** (already done):
```
aiogram==3.4.1
asyncpg==0.29.0
python-dotenv==1.0.0
```

2. **Create `Procfile`** (already done):
```
web: python bot.py
```

### 2. Deploy to Render

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service** on Render
3. **Configure environment variables**:
   - `BOT_TOKEN`: Your Telegram bot token
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ADMIN_ID`: Your Telegram user ID

4. **Deploy**: Render will automatically build and deploy your bot

### 3. Database Setup on Render

1. **Create a PostgreSQL database** on Render
2. **Copy the database URL** to your environment variables
3. **The bot will automatically initialize** the database schema

## ⚙️ Configuration

All bot settings are stored in the database and can be modified by admins:

| Setting | Default | Description |
|---------|---------|-------------|
| `currency_symbol` | ₦ | Currency symbol for display |
| `min_withdrawal` | 1000 | Minimum withdrawal amount |
| `daily_bonus` | 100 | Daily bonus amount |
| `referral_reward` | 50 | Reward for successful referrals |
| `dice_cooldown` | 300 | Seconds between dice rolls |
| `max_daily_rolls` | 10 | Maximum dice rolls per day |

## 🎮 Bot Commands

### User Commands
- `/start` - Start the bot and register
- `🎲 Play Game` - Play dice game
- `💰 Balance` - Check balance
- `👤 Profile` - View profile
- `💸 Withdraw` - Request withdrawal
- `📜 Transactions` - View transaction history
- `👥 Referrals` - Get referral link
- `🎁 Daily Bonus` - Claim daily bonus
- `ℹ️ Help` - Show help information

### Admin Commands
- `⚙️ Admin Panel` - Access admin controls
- Admin panel includes:
  - User management
  - Withdrawal approval
  - Settings configuration
  - Broadcasting
  - Statistics

## 🔧 Database Schema

### Users Table
- `id` - Primary key
- `user_id` - Telegram user ID
- `username` - Telegram username
- `balance` - Current balance
- `total_earned` - Lifetime earnings
- `referral_count` - Number of referrals
- `referrer_id` - ID of user who referred them
- `join_date` - Account creation date

### Transactions Table
- `id` - Primary key
- `user_id` - User who made the transaction
- `transaction_type` - Type (game, bonus, referral, withdrawal)
- `amount` - Transaction amount
- `description` - Transaction description
- `created_at` - Transaction timestamp

### Game History Table
- `id` - Primary key
- `user_id` - User who played
- `dice_value` - Dice roll result
- `reward` - Reward earned
- `played_at` - Game timestamp

### Withdraw Requests Table
- `id` - Primary key
- `user_id` - User requesting withdrawal
- `amount` - Withdrawal amount
- `status` - pending/paid/rejected
- `created_at` - Request timestamp
- `processed_at` - Processing timestamp

### Config Table
- `id` - Primary key
- `key` - Configuration key
- `value` - Configuration value
- `updated_at` - Last update timestamp

## 🛡️ Security Features

- **Rate Limiting**: Prevents spam and abuse
- **Input Validation**: All user inputs are validated
- **Admin Controls**: Sensitive operations require admin privileges
- **Transaction Logging**: Complete audit trail
- **Error Handling**: Comprehensive error handling and logging

## 📊 Monitoring

The bot includes comprehensive logging:
- **File Logging**: Daily log files
- **Console Logging**: Real-time error monitoring
- **Transaction Tracking**: All financial operations logged
- **User Activity**: Registration and game activity logged

## 🔄 Future Expansion

The modular architecture supports easy expansion:
- **New Games**: Add new game types in `handlers/games.py`
- **Reward Systems**: Extend reward mechanisms
- **Payment Methods**: Add more withdrawal options
- **Analytics**: Enhanced statistics and reporting

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check `DATABASE_URL` in environment variables
   - Ensure PostgreSQL is running and accessible

2. **Bot Not Responding**:
   - Verify `BOT_TOKEN` is correct
   - Check bot logs for errors

3. **Admin Commands Not Working**:
   - Verify `ADMIN_ID` is set correctly
   - Ensure you're using the correct Telegram user ID

### Logs

Check the log files for detailed error information:
- Local: `bot_YYYYMMDD.log`
- Render: Check the Render dashboard logs

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support or questions, please contact the admin or create an issue in the repository.

---

**Happy Gaming! 🎲🎉**