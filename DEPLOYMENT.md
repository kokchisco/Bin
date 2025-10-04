# 🚀 Deployment Guide

This guide will help you deploy your Telegram bot to Render and set up the database.

## 📋 Prerequisites

1. **Telegram Bot Token**: Get one from [@BotFather](https://t.me/BotFather)
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **PostgreSQL Database**: We'll use Render's managed PostgreSQL
4. **GitHub Repository**: Push your code to GitHub

## 🔧 Step 1: Prepare Your Bot

### 1.1 Get Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command
3. Follow the prompts to create your bot
4. Save the bot token (you'll need it later)

### 1.2 Get Your Admin ID
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your user ID (you'll need this for admin access)

## 🗄️ Step 2: Set Up Database

### 2.1 Create PostgreSQL Database on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "PostgreSQL"
3. Choose a name (e.g., "telegram-bot-db")
4. Select the free tier
5. Click "Create Database"
6. Wait for the database to be created
7. Copy the **External Database URL** (you'll need this)

### 2.2 Test Database Connection
```bash
# Install dependencies locally
pip install -r requirements.txt

# Test database connection
python test_bot.py
```

## 🚀 Step 3: Deploy to Render

### 3.1 Create Web Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Choose your repository

### 3.2 Configure Web Service
Use these settings:

**Basic Settings:**
- **Name**: `telegram-bot` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (optional)

### 3.3 Set Environment Variables
In the Render dashboard, go to your service → Environment:

```env
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://username:password@host:port/database
ADMIN_ID=your_telegram_user_id
```

**Important**: Replace the values with your actual:
- Bot token from @BotFather
- Database URL from your PostgreSQL service
- Your Telegram user ID

### 3.4 Deploy
1. Click "Create Web Service"
2. Wait for the build to complete (usually 2-3 minutes)
3. Check the logs for any errors

## ✅ Step 4: Verify Deployment

### 4.1 Check Bot Status
1. Go to your bot's logs in Render dashboard
2. Look for "Bot started successfully!" message
3. If you see errors, check the troubleshooting section

### 4.2 Test Bot Functionality
1. Find your bot on Telegram (search for the username you set)
2. Send `/start` command
3. Test the main menu buttons
4. Verify admin panel works (if you're the admin)

## 🔧 Step 5: Initial Configuration

### 5.1 Set Up Admin Panel
1. Start a chat with your bot
2. Use the admin panel to configure:
   - Currency symbol (e.g., $, €, ₦)
   - Minimum withdrawal amount
   - Daily bonus amount
   - Referral rewards

### 5.2 Test All Features
- ✅ User registration
- ✅ Dice game
- ✅ Daily bonus
- ✅ Balance checking
- ✅ Transaction history
- ✅ Referral system
- ✅ Withdrawal requests
- ✅ Admin panel

## 🛠️ Troubleshooting

### Common Issues

**1. Bot Not Responding**
- Check if BOT_TOKEN is correct
- Verify the bot is running (check logs)
- Ensure webhook is not set (we use polling)

**2. Database Connection Error**
- Verify DATABASE_URL is correct
- Check if database is running
- Ensure database URL includes SSL parameters

**3. Admin Panel Not Working**
- Verify ADMIN_ID is correct
- Check if you're using the right Telegram account
- Restart the bot if needed

**4. Bot Crashes on Startup**
- Check logs for specific error messages
- Verify all environment variables are set
- Ensure all dependencies are installed

### Debug Commands

**Check Bot Status:**
```bash
# In Render logs, look for:
"Bot started successfully!"
"Database tables created/verified"
```

**Test Database:**
```bash
# Run locally to test database
python test_bot.py
```

**View Logs:**
- Go to Render dashboard → Your service → Logs
- Look for error messages or warnings

## 📊 Monitoring

### 4.1 Health Checks
- Monitor bot logs regularly
- Check database connection status
- Verify user registrations are working

### 4.2 Performance Monitoring
- Monitor response times
- Check memory usage
- Watch for rate limiting issues

### 4.3 User Support
- Monitor withdrawal requests
- Check for user complaints
- Review transaction logs

## 🔄 Updates and Maintenance

### Updating the Bot
1. Push changes to GitHub
2. Render will automatically redeploy
3. Monitor logs for any issues

### Database Maintenance
- Regular backups (Render handles this)
- Monitor database performance
- Clean up old logs if needed

### Configuration Updates
- Use admin panel for most changes
- Restart bot for major configuration changes
- Monitor impact of changes

## 🚨 Security Considerations

### 1. Environment Variables
- Never commit `.env` file to Git
- Use strong, unique tokens
- Rotate tokens regularly

### 2. Database Security
- Use strong database passwords
- Enable SSL connections
- Regular security updates

### 3. Bot Security
- Monitor for abuse
- Implement rate limiting
- Regular security audits

## 📈 Scaling

### When to Scale
- High user count (>1000 active users)
- Slow response times
- Database performance issues

### Scaling Options
1. **Upgrade Render Plan**: Move to paid tier
2. **Database Optimization**: Add indexes, optimize queries
3. **Caching**: Implement Redis for frequently accessed data
4. **Load Balancing**: Multiple bot instances

## 🆘 Support

### Getting Help
1. Check the logs first
2. Review this documentation
3. Check GitHub issues
4. Contact support if needed

### Useful Resources
- [Render Documentation](https://render.com/docs)
- [aiogram Documentation](https://docs.aiogram.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**🎉 Congratulations! Your Telegram bot is now live and ready to serve users!**