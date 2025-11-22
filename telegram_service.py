from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from datetime import datetime
from config import Config
from database import Database
from task_parser import TaskParser
import asyncio
import httpx
from gtts import gTTS
import tempfile
import os

class TelegramService:
    """Service for Telegram bot messaging (FREE alternative to WhatsApp)"""
    
    def __init__(self, database: Database, task_parser: TaskParser):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.database = database
        self.task_parser = task_parser
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """👋 Welcome to Reminder Bot!

Send me a message like:
• "Remind me to buy milk tomorrow at 9 AM"
• "Remind me to call mom before Friday morning"
• "Remind me to submit report on Thursday"

I'll understand when you want to be reminded and send you a notification!

Commands:
/start - Show this message
/list - View your pending reminders
/help - Get help"""
        
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """🤖 How to use Reminder Bot:

Just send me a natural message about what you want to be reminded about!

Examples:
• "Remind me to buy petrol before Friday morning"
• "Remind me to workout tomorrow"
• "Remind me about the meeting in 2 hours"

I'll figure out when to remind you and send a message at the right time!"""
        
        await update.message.reply_text(help_text)
    
    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command"""
        user_id = str(update.effective_user.id)
        tasks = self.database.get_user_tasks(user_id)
        
        if not tasks:
            await update.message.reply_text("📋 You have no pending reminders.")
        else:
            task_list = "📋 Your pending reminders:\n\n"
            for i, task in enumerate(tasks, 1):
                task_list += f"{i}. {task.task_description}\n   ⏰ {task.reminder_time.strftime('%A, %B %d at %I:%M %p')}\n\n"
            await update.message.reply_text(task_list)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = None
        try:
            message_text = update.message.text
            user_id = str(update.effective_user.id)
            user_name = update.effective_user.first_name or "User"
            
            print(f"📨 Received message from {user_name} ({user_id}): {message_text}")
            
            # Parse the message
            parsed_data = self.task_parser.parse_message(message_text)
            print(f"🔍 Parsed data: {parsed_data}")
            
            if not parsed_data:
                # Try fallback parser
                parsed_data = self.task_parser.parse_simple_reminder(message_text)
            
            if not parsed_data:
                error_msg = "❌ I couldn't understand when you want to be reminded.\n\nTry something like: 'Remind me to [task] on [day] at [time]'"
                await update.message.reply_text(error_msg)
                return
            
            # Save the task
            task = self.database.add_task(
                user_phone=user_id,
                task_description=parsed_data['task_description'],
                reminder_time=parsed_data['reminder_time']
            )
            
            # Send confirmation
            reminder_time_str = parsed_data['reminder_time'].strftime('%A, %B %d at %I:%M %p')
            confirmation = f"✅ Got it! I'll remind you to:\n\n'{parsed_data['task_description']}'\n\nat {reminder_time_str}"
            
            await update.message.reply_text(confirmation)
            
            print(f"✅ Created task {task.id} for {user_name}")
            
        except Exception as e:
            print(f"❌ Error handling message: {e}")
            # Try to send error message, but don't crash if it fails
            try:
                await update.message.reply_text("❌ An error occurred. Please try again.")
            except Exception as reply_error:
                print(f"❌ Could not send error message to user: {reply_error}")
    
    async def send_reminder(self, user_id: str, task_description: str):
        """Send a voice reminder message to a user"""
        try:
            # First send text message
            message = f"🔔 Reminder: {task_description}"
            await self.application.bot.send_message(
                chat_id=int(user_id),
                text=message
            )
            
            # Generate and send voice message
            try:
                # Create voice message text
                voice_text = f"Reminder: {task_description}"
                
                # Generate speech
                tts = gTTS(text=voice_text, lang='en', slow=False)
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                    temp_path = temp_file.name
                    tts.save(temp_path)
                
                # Send voice message
                with open(temp_path, 'rb') as voice_file:
                    await self.application.bot.send_voice(
                        chat_id=int(user_id),
                        voice=voice_file,
                        caption=f"🔊 Voice reminder"
                    )
                
                # Clean up temporary file
                os.unlink(temp_path)
                print(f"📢 Sent voice reminder for: {task_description}")
                
            except Exception as voice_error:
                print(f"⚠️ Could not send voice message: {voice_error}")
                # Text message was already sent, so still return True
            
            return True
        except Exception as e:
            print(f"❌ Error sending reminder to {user_id}: {e}")
            return False
    
    def start_bot(self):
        """Start the Telegram bot"""
        print("🤖 Starting Telegram bot...")
        
        # Create application with increased timeout to handle network issues better
        request = HTTPXRequest(
            connection_pool_size=8,
            connect_timeout=10.0,
            read_timeout=20.0,
            write_timeout=20.0,
            pool_timeout=10.0
        )
        
        self.application = Application.builder().token(self.bot_token).request(request).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("list", self.list_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start polling
        print("✅ Telegram bot started! Send a message to your bot.")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
