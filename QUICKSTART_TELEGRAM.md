# 🚀 Quick Start - Telegram Bot (FREE)

Get your reminder bot running in **2 minutes** - completely FREE!

## Step 1: Create Your Bot (30 seconds)

1. Open **Telegram** app
2. Search for **@BotFather**
3. Send: `/newbot`
4. Give it a name: `My Reminder Bot`
5. Give it a username: `my_reminder_bot` (must end with 'bot')
6. **Copy the token** (looks like: `123456789:ABCdefGHI...`)

## Step 2: Get OpenAI Key (1 minute)

1. Go to https://platform.openai.com/api-keys
2. Sign up (free tier includes $5 credit)
3. Click **Create new secret key**
4. **Copy the key** (starts with `sk-...`)

## Step 3: Run Setup Script (30 seconds)

```powershell
cd "C:\Users\GIHAN LAKMAL\whatsapp-reminder-bot"
.\setup_telegram.ps1
```

The script will:
- Create virtual environment
- Install all dependencies
- Create `.env` file
- Prompt you to add your tokens

## Step 4: Configure .env

When prompted, add your tokens to `.env`:

```env
MESSAGING_PLATFORM=telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...  # From BotFather
OPENAI_API_KEY=sk-...                       # From OpenAI
DEFAULT_TIMEZONE=Asia/Kolkata               # Your timezone
```

## Step 5: Start the Bot

```powershell
python app_telegram.py
```

You should see:
```
🤖 Telegram Reminder Bot - FREE Version
✅ Using FREE Telegram messaging
✅ Telegram bot started!
```

## Step 6: Test Your Bot

1. Open Telegram
2. Search for your bot: `@my_reminder_bot`
3. Click **Start**
4. Send: `Remind me to test this tomorrow at 9 AM`
5. You'll get a confirmation!

## Example Messages

Try these:
```
Remind me to buy milk tomorrow at 9 AM
Remind me to call mom before Friday morning
Remind me about the meeting in 2 hours
Remind me to workout on Thursday
```

## Commands

- `/start` - Welcome message
- `/help` - Show help
- `/list` - View pending reminders

## Troubleshooting

**Bot doesn't respond?**
- Make sure `app_telegram.py` is running
- Check your bot token in `.env`
- Try `/start` command

**"Invalid token" error?**
- Double-check token from BotFather
- No extra spaces in `.env`

**OpenAI errors?**
- Verify API key is correct
- Check you have credits: https://platform.openai.com/usage

## Costs

- ✅ **Telegram**: FREE forever
- ✅ **OpenAI**: $5 free credit (enough for ~5000 reminders)
- ✅ **No credit card** required for testing

## Next Steps

Once it's working:

1. **Keep it running** - Use a server for 24/7 operation
   - Free options: Railway.app, Render.com, Fly.io
   
2. **Invite friends** - Share your bot username

3. **Add features** - Check README.md for ideas

## Full Documentation

- **[TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)** - Detailed setup guide
- **[FREE_vs_PAID.md](FREE_vs_PAID.md)** - Why Telegram is better
- **[README.md](README.md)** - Complete documentation

## Support

Questions? Check:
- Error messages in console
- TELEGRAM_SETUP.md
- README.md

---

**That's it!** You now have a FREE AI-powered reminder bot! 🎉
