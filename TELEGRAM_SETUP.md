# 🎉 FREE Setup Guide - Using Telegram Bot

This guide will help you set up the reminder bot using **Telegram** (completely FREE - no payment required!)

## Why Telegram Instead of WhatsApp?

- ✅ **100% FREE** - No payment required
- ✅ **Easy Setup** - Just 2 minutes to get started
- ✅ **No Phone Number** - Works with any Telegram account
- ✅ **Same Features** - All reminder functionality works the same way

## Step-by-Step Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to BotFather
3. Follow the instructions:
   - Choose a name for your bot (e.g., "My Reminder Bot")
   - Choose a username (must end in 'bot', e.g., "my_reminder_bot")
4. BotFather will give you a **TOKEN** - save this!
   - It looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. Install Dependencies

```powershell
# Navigate to project directory
cd "C:\Users\GIHAN LAKMAL\whatsapp-reminder-bot"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies (includes python-telegram-bot)
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy the example config:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` file:
   ```env
   # OpenAI API Key (required)
   OPENAI_API_KEY=sk-your-key-here
   
   # Use Telegram (FREE!)
   MESSAGING_PLATFORM=telegram
   
   # Your Telegram Bot Token from BotFather
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   
   # Your timezone
   DEFAULT_TIMEZONE=Asia/Kolkata
   ```

### 4. Get OpenAI API Key

You still need an OpenAI API key for natural language processing:

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy it to your `.env` file

**Note:** OpenAI has a free tier with $5 credit for new users. Each reminder parsing costs ~$0.001, so you can process ~5000 reminders for free!

### 5. Run the Bot

```powershell
python app_telegram.py
```

You should see:
```
🤖 Telegram Reminder Bot - FREE Version
✅ Using FREE Telegram messaging
⏰ Timezone: Asia/Kolkata
✅ Telegram bot started! Send a message to your bot.
```

### 6. Start Using Your Bot

1. Open Telegram
2. Search for your bot by username (e.g., `@my_reminder_bot`)
3. Click **Start** or send `/start`
4. Send a reminder like: `Remind me to buy milk tomorrow at 9 AM`

## Available Commands

- `/start` - Welcome message and instructions
- `/help` - Show help
- `/list` - View your pending reminders
- Just send any natural language reminder message!

## Examples

```
Remind me to buy petrol before Friday morning
Remind me to call mom tomorrow at 6 PM
Remind me to workout in 2 hours
Remind me about the meeting on Thursday
```

## How It Works

1. You send a message to your Telegram bot
2. The bot uses AI (LangChain + OpenAI) to understand your message
3. It extracts the task and calculates when to remind you
4. Stores it in the database
5. A background scheduler checks every minute
6. Sends you a Telegram message at the right time!

## Troubleshooting

### Bot doesn't respond
- Make sure `app_telegram.py` is running
- Check that your bot token is correct in `.env`
- Try stopping and restarting the bot

### "Invalid token" error
- Double-check your token from BotFather
- Make sure there are no extra spaces in `.env`
- Token format should be: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Reminders not being sent
- Check that the scheduler started (you should see "Reminder scheduler started")
- Verify database has tasks: they should appear when you use `/list`
- Check the timezone in your `.env` file

### OpenAI errors
- Verify your API key is correct
- Check you have credits available at https://platform.openai.com/usage
- Free tier includes $5 credit (enough for ~5000 reminders!)

## Cost Comparison

| Platform | Setup Cost | Monthly Cost | Notes |
|----------|-----------|--------------|-------|
| **Telegram** | **FREE** | **FREE** | ✅ Recommended! |
| WhatsApp (Twilio) | $0 | ~$20/month | Need business verification |
| SMS (Twilio) | $0 | ~$0.0075/msg | Pay per message |

## Next Steps

Once your bot is working:

1. **Deploy to a server** so it runs 24/7:
   - Free options: Railway.app, Render.com, Fly.io
   - Cheap VPS: DigitalOcean ($4/month), Linode, Vultr

2. **Add features**:
   - Recurring reminders
   - Snooze functionality
   - Edit/delete reminders
   - Share reminders with friends

3. **Improve parsing**:
   - Add support for more languages
   - Better time zone handling
   - Voice message support

## Support

If you have questions:
- Check the main `README.md`
- Review the error messages in the console
- Make sure all dependencies are installed

---

**Enjoy your FREE reminder bot!** 🎉

No payment required, no credit card, no phone number verification - just install and use!
