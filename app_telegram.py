"""
Telegram Bot Application - FREE Alternative
This version uses Telegram instead of WhatsApp (no payment required!)
"""

from config import Config
from database import Database
from task_parser import TaskParser
from telegram_service import TelegramService
from scheduler import ReminderScheduler
import asyncio
from threading import Thread

# Initialize services
database = Database()
task_parser = TaskParser()
telegram_service = TelegramService(database, task_parser)

class TelegramReminderScheduler(ReminderScheduler):
    """Modified scheduler for Telegram"""
    
    def __init__(self, database: Database, telegram_service: TelegramService):
        self.database = database
        self.telegram_service = telegram_service
        from apscheduler.schedulers.background import BackgroundScheduler
        import pytz
        self.scheduler = BackgroundScheduler()
        self.timezone = pytz.timezone(Config.DEFAULT_TIMEZONE)
    
    def check_and_send_reminders(self):
        """Check database for pending reminders and send them via Telegram"""
        try:
            from datetime import datetime
            current_time = datetime.now(self.timezone)
            
            pending_tasks = self.database.get_pending_reminders(current_time)
            
            if pending_tasks:
                print(f"📬 Found {len(pending_tasks)} pending reminders to send")
            
            for task in pending_tasks:
                try:
                    # Send reminder via Telegram using the bot's application
                    # Create a coroutine and schedule it on the bot's event loop
                    async def send():
                        return await self.telegram_service.send_reminder(
                            task.user_phone,
                            task.task_description
                        )
                    
                    # Use asyncio.run_coroutine_threadsafe to send from background thread
                    try:
                        # Get the bot's running event loop
                        loop = self.telegram_service.application._application.loop
                        if loop and loop.is_running():
                            future = asyncio.run_coroutine_threadsafe(send(), loop)
                            success = future.result(timeout=10)
                        else:
                            print(f"⚠️ Event loop not available, skipping task {task.id}")
                            continue
                    except Exception as loop_error:
                        print(f"⚠️ Could not access event loop: {loop_error}")
                        continue
                    
                    if success:
                        self.database.mark_task_sent(task.id)
                        print(f"✅ Sent reminder for task {task.id}")
                    else:
                        print(f"❌ Failed to send reminder for task {task.id}")
                        
                except Exception as e:
                    print(f"❌ Error sending reminder for task {task.id}: {e}")
            
        except Exception as e:
            print(f"❌ Error in reminder checker: {e}")

def main():
    """Main entry point for Telegram bot"""
    try:
        # Validate configuration
        Config.validate()
        
        print("=" * 60)
        print("🤖 Telegram Reminder Bot - FREE Version")
        print("=" * 60)
        print(f"✅ Using FREE Telegram messaging")
        print(f"⏰ Timezone: {Config.DEFAULT_TIMEZONE}")
        print("=" * 60)
        print()
        
        # Start the reminder scheduler in a separate thread
        reminder_scheduler = TelegramReminderScheduler(database, telegram_service)
        reminder_scheduler.start()
        
        # Start the Telegram bot (this will block)
        telegram_service.start_bot()
        
    except KeyboardInterrupt:
        print("\n⏹️ Shutting down...")
        reminder_scheduler.stop()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
