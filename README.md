# Reminder Bot 🤖📱

An intelligent reminder bot that understands natural language to create and send reminders at the right time.

## 🎉 FREE Version Available!

**NEW:** Use **Telegram** instead of WhatsApp - completely FREE, no payment required!

See **[TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)** for the free setup guide.

## Features

- 🗣️ **Natural Language Processing**: Uses LangChain + OpenAI to understand reminder requests
- 📅 **Smart Time Parsing**: Understands phrases like "before Friday morning", "tomorrow at 6 PM", etc.
- 🔔 **Automated Reminders**: Background scheduler sends reminders at the specified time
- 💾 **Persistent Storage**: SQLite database stores all tasks and reminders
- 📱 **Multiple Platforms**: 
  - **Telegram** (FREE!) - Recommended
  - WhatsApp (via Twilio, paid) - Optional

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  WhatsApp   │────────▶│  Flask App   │────────▶│  LangChain  │
│   (Twilio)  │◀────────│  (Webhook)   │◀────────│   Parser    │
└─────────────┘         └──────────────┘         └─────────────┘
                              │      │
                              ▼      ▼
                        ┌──────────┐  ┌───────────┐
                        │ Database │  │ Scheduler │
                        │ (SQLite) │  │(APScheduler)│
                        └──────────┘  └───────────┘
```

## Quick Start (Telegram - FREE!)

**Recommended for most users - no payment required!**

See **[TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)** for complete FREE setup guide.

Quick steps:
1. Create a Telegram bot via @BotFather
2. Get your bot token
3. Configure `.env` with your token
4. Run `python app_telegram.py`
5. Start chatting with your bot!

## Setup (WhatsApp - Paid Option)

### 1. Prerequisites

- Python 3.8 or higher
- Twilio account with WhatsApp enabled (paid)
- OpenAI API key

### 2. Installation

```powershell
# Clone or navigate to the project directory
cd whatsapp-reminder-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```powershell
Copy-Item .env.example .env
```

Edit `.env` with your credentials:

```env
# Get this from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-...

# Get these from https://console.twilio.com/
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Your timezone (e.g., Asia/Kolkata, America/New_York)
DEFAULT_TIMEZONE=Asia/Kolkata
```

### 4. Set up Twilio WhatsApp

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Follow the instructions to activate your Twilio WhatsApp sandbox
4. Configure the webhook URL to point to your Flask app: `https://your-domain.com/webhook`

### 5. Run the Application

```powershell
# Make sure virtual environment is activated
python app.py
```

The app will start on `http://localhost:5000`

## Usage

### Basic Reminder

Send a WhatsApp message to your Twilio number:

```
Remind me to buy petrol before Friday morning
```

The bot will:
1. Parse your message using AI
2. Calculate the appropriate reminder time (e.g., Thursday 8 PM)
3. Store the task in the database
4. Send you a confirmation
5. Remind you at the scheduled time

### Commands

- **`help`** or **`start`**: Get usage instructions
- **`list`**: View all your pending reminders
- Any natural language reminder request

### Examples

```
Remind me to call mom tomorrow at 6 PM
Remind me to submit report on Thursday
Remind me to take medicine in 2 hours
Remind me about the meeting before Monday morning
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/webhook` | POST | Receive WhatsApp messages (Twilio webhook) |
| `/health` | GET | Health check and scheduler status |
| `/tasks/<phone>` | GET | Get tasks for a user (admin) |

## Project Structure

```
whatsapp-reminder-bot/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── database.py            # SQLAlchemy models and database operations
├── task_parser.py         # LangChain-based NLP parser
├── whatsapp_service.py    # Twilio WhatsApp messaging
├── scheduler.py           # Background reminder scheduler
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## How It Works

### 1. Message Reception
When a user sends a WhatsApp message, Twilio forwards it to the `/webhook` endpoint.

### 2. Natural Language Processing
The `TaskParser` uses LangChain with OpenAI's GPT-3.5 to:
- Extract the task description
- Parse relative time expressions (tomorrow, Friday, before morning, etc.)
- Calculate the exact reminder datetime
- Handle edge cases and ambiguities

### 3. Task Storage
Tasks are stored in SQLite with:
- User's phone number
- Task description
- Reminder datetime
- Sent status

### 4. Reminder Scheduling
A background scheduler (`APScheduler`) runs every minute to:
- Query the database for pending reminders
- Send WhatsApp messages for reminders whose time has arrived
- Mark tasks as sent

## Development

### Running Tests

```powershell
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest
```

### Debugging

Enable debug mode in `.env`:

```env
FLASK_DEBUG=True
```

Check logs for detailed information about:
- Incoming messages
- Parsing results
- Reminder sending
- Scheduler activity

## Deployment

### Using ngrok (for testing)

```powershell
# Install ngrok from https://ngrok.com/
ngrok http 5000
```

Use the ngrok URL as your Twilio webhook URL.

### Production Deployment

For production, deploy to:
- **Heroku**: Use `Procfile` with gunicorn
- **AWS/Azure/GCP**: Use Docker or VM
- **PythonAnywhere**: Configure WSGI app

Make sure to:
1. Use a production database (PostgreSQL recommended)
2. Set `FLASK_ENV=production`
3. Use HTTPS for webhook URL
4. Set up proper monitoring and logging

## Troubleshooting

### Reminders not being sent

1. Check scheduler status: `GET /health`
2. Verify database has tasks: Check `reminders.db`
3. Ensure Twilio credentials are correct
4. Check timezone configuration

### Message parsing fails

1. Verify OpenAI API key is valid
2. Check API quota/rate limits
3. Review message format
4. Check logs for parsing errors

### WhatsApp messages not received

1. Verify Twilio webhook URL is correct and accessible
2. Check Twilio logs in console
3. Ensure webhook uses POST method
4. Verify SSL certificate (production)

## Contributing

Contributions are welcome! Areas for improvement:
- Add support for recurring reminders
- Implement task editing/deletion
- Add more natural language patterns
- Support for multiple languages
- Voice message support

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues or questions:
- Create an issue in the repository
- Check Twilio documentation: https://www.twilio.com/docs/whatsapp
- Review LangChain docs: https://python.langchain.com/

---

Made with ❤️ using Flask, LangChain, and Twilio
