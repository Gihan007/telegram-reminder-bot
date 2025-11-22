from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from database import Database
from whatsapp_service import WhatsAppService
import pytz
from config import Config

class ReminderScheduler:
    """Background scheduler for sending reminders"""
    
    def __init__(self, database: Database, whatsapp_service: WhatsAppService):
        self.database = database
        self.whatsapp_service = whatsapp_service
        self.scheduler = BackgroundScheduler()
        self.timezone = pytz.timezone(Config.DEFAULT_TIMEZONE)
    
    def start(self):
        """Start the background scheduler"""
        # Check for pending reminders every minute
        self.scheduler.add_job(
            self.check_and_send_reminders,
            'interval',
            minutes=1,
            id='reminder_checker'
        )
        self.scheduler.start()
        print("✅ Reminder scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("⏹️ Reminder scheduler stopped")
    
    def check_and_send_reminders(self):
        """Check database for pending reminders and send them"""
        try:
            current_time = datetime.now(self.timezone)
            
            # Get all pending reminders that should be sent now
            pending_tasks = self.database.get_pending_reminders(current_time)
            
            if pending_tasks:
                print(f"📬 Found {len(pending_tasks)} pending reminders to send")
            
            for task in pending_tasks:
                try:
                    # Send the reminder
                    success = self.whatsapp_service.send_reminder(
                        task.user_phone,
                        task.task_description
                    )
                    
                    if success:
                        # Mark as sent in database
                        self.database.mark_task_sent(task.id)
                        print(f"✅ Sent reminder for task {task.id} to {task.user_phone}")
                    else:
                        print(f"❌ Failed to send reminder for task {task.id}")
                        
                except Exception as e:
                    print(f"❌ Error sending reminder for task {task.id}: {e}")
            
        except Exception as e:
            print(f"❌ Error in reminder checker: {e}")
    
    def get_scheduler_status(self):
        """Get current scheduler status"""
        return {
            'running': self.scheduler.running,
            'jobs': [
                {
                    'id': job.id,
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None
                }
                for job in self.scheduler.get_jobs()
            ]
        }
