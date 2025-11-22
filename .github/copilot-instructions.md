# AI Agent Instructions for Reminder Bot

## Project Overview
This is a reminder bot that uses natural language processing (LangChain + OpenAI) to understand user reminder requests. Supports both **Telegram (FREE)** and WhatsApp (paid) platforms.

## Architecture Pattern

### Telegram (Recommended - FREE)
- **Message Flow**: Telegram → Bot API → LangChain parser → SQLite storage → APScheduler → Telegram notification
- **Key Components**: Telegram app (`app_telegram.py`), Telegram service (`telegram_service.py`), NLP parser (`task_parser.py`), database (`database.py`), scheduler

### WhatsApp (Paid Option)
- **Message Flow**: WhatsApp → Twilio → Flask webhook → LangChain parser → SQLite storage → APScheduler → WhatsApp notification
- **Key Components**: Flask app (`app.py`), WhatsApp service (`whatsapp_service.py`), NLP parser, database, scheduler

## Development Workflow

### Setup & Running

**For Telegram (FREE - Recommended):**
```powershell
# Run the setup script
.\setup_telegram.ps1

# Or manually:
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with TELEGRAM_BOT_TOKEN and OPENAI_API_KEY
python app_telegram.py
```

**For WhatsApp (Paid):**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with Twilio credentials
python app.py
```

### Testing Locally
- Use **ngrok** to expose local Flask app: `ngrok http 5000`
- Configure ngrok URL in Twilio webhook settings
- Send test messages to Twilio WhatsApp sandbox number

## Code Conventions

### Time Handling
- Always use timezone-aware datetime objects via `pytz`
- Default timezone configured in `Config.DEFAULT_TIMEZONE`
- When parsing times, ensure they're in the future (add 1 day if parsed time is in the past)

### Database Operations
- Use context managers or try-finally blocks with `session.close()`
- All task queries should filter by `is_sent=False` for pending reminders
- Example: `database.get_pending_reminders(current_time)`

### LangChain Prompting
- Prompts in `task_parser.py` use structured JSON output format
- Always include current datetime context in prompts
- Handle "before [time]" vs "on [time]" semantics (before = earlier reminder, on = exact time)
- Fall back to simple regex parsing if LLM parsing fails

### WhatsApp Messaging
- Phone numbers must use format `whatsapp:+1234567890`
- Emojis are used for visual feedback (✅ confirmation, 🔔 reminder, ❌ error)
- Keep messages concise due to WhatsApp character limits

## Key Files

### `app.py` - Main Flask Application
- `/webhook` endpoint: Receives WhatsApp messages from Twilio
- Handles commands: `help`, `list`, or natural language reminder requests
- Initializes and starts background scheduler on app startup

### `task_parser.py` - NLP Parser
- Uses LangChain with GPT-3.5 to extract task description and reminder time
- Converts relative dates (tomorrow, Friday, etc.) to absolute datetime
- Includes fallback regex-based parser for simple patterns

### `database.py` - Data Layer
- SQLAlchemy ORM with `Task` model
- Critical fields: `user_phone`, `task_description`, `reminder_time`, `is_sent`
- Key methods: `add_task()`, `get_pending_reminders()`, `mark_task_sent()`

### `scheduler.py` - Background Scheduler
- APScheduler runs `check_and_send_reminders()` every 1 minute
- Queries pending tasks where `reminder_time <= now` and `is_sent=False`
- Sends WhatsApp notification and marks task as sent

### `whatsapp_service.py` - Twilio Integration
- Wraps Twilio Client for sending messages
- Methods: `send_reminder()`, `send_confirmation()`, `send_error()`

## Common Tasks

### Adding New Command
1. Add handler in `app.py` webhook endpoint before message parsing
2. Pattern: `if incoming_msg.lower() == 'your_command':`
3. Send response via `whatsapp_service.send_message()`

### Modifying Time Parsing Logic
1. Edit prompt template in `task_parser.py` constructor
2. Update rules in the prompt's "Important rules" section
3. Test with various natural language inputs

### Changing Reminder Check Interval
1. Modify `scheduler.py` in `start()` method
2. Change `minutes=1` parameter in `scheduler.add_job()`
3. Note: More frequent checks = higher resource usage

### Adding Database Fields
1. Add column to `Task` model in `database.py`
2. Add field to `to_dict()` method
3. Delete existing `reminders.db` to recreate schema

## Environment Variables

### For Telegram (FREE):
- **Required**: `OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `MESSAGING_PLATFORM=telegram`
- **Optional**: `DEFAULT_TIMEZONE`, `DATABASE_URL`

### For WhatsApp (Paid):
- **Required**: `OPENAI_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `MESSAGING_PLATFORM=whatsapp`
- **Optional**: `DEFAULT_TIMEZONE`, `DATABASE_URL`, `FLASK_DEBUG`

- Validate config on startup with `Config.validate()`

## Error Handling
- Always wrap external API calls (OpenAI, Twilio) in try-except
- Log errors with descriptive messages using `print()` (consider adding proper logging library)
- Send user-friendly error messages via WhatsApp when parsing fails

## Testing Strategy
- Test message parsing with edge cases: "tomorrow", "in 2 hours", "before Friday morning"
- Verify timezone handling for different user timezones
- Test scheduler by creating tasks with `reminder_time` in the next 2 minutes
- Use `/health` endpoint to verify scheduler is running

## Deployment Considerations
- **Database**: Switch from SQLite to PostgreSQL for production (`DATABASE_URL`)
- **Process Management**: Use gunicorn or uWSGI instead of Flask dev server
- **HTTPS Required**: Twilio webhooks require SSL certificate
- **Background Worker**: Ensure scheduler process stays alive (consider separate worker process)

## Common Pitfalls
- Forgetting to activate virtual environment before running
- Not configuring Twilio webhook URL correctly (must be publicly accessible)
- Timezone mismatches causing reminders at wrong times
- Database session not closed properly (memory leaks)
- OpenAI API rate limits during high usage

## Extending the Bot
- **Recurring Reminders**: Add `recurrence_pattern` field and modify scheduler logic
- **Task Editing**: Add command like "edit reminder 3" and parse task ID
- **Multiple Languages**: Pass user language to LangChain prompt
- **Voice Messages**: Use Twilio's media handling for audio input
