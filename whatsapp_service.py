from twilio.rest import Client
from config import Config

class WhatsAppService:
    """Service for sending WhatsApp messages via Twilio"""
    
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.from_number = Config.TWILIO_WHATSAPP_NUMBER
    
    def send_message(self, to_number, message):
        """
        Send a WhatsApp message to a user
        
        Args:
            to_number: Phone number in format 'whatsapp:+1234567890'
            message: Message text to send
        
        Returns:
            Message SID if successful, None otherwise
        """
        try:
            # Ensure number is in correct format
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return message.sid
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return None
    
    def send_reminder(self, to_number, task_description):
        """Send a reminder message"""
        message = f"🔔 Reminder: {task_description}"
        return self.send_message(to_number, message)
    
    def send_confirmation(self, to_number, task_description, reminder_time):
        """Send a confirmation message after task creation"""
        message = f"✅ Got it! I'll remind you to:\n\n'{task_description}'\n\nat {reminder_time}"
        return self.send_message(to_number, message)
    
    def send_error(self, to_number, error_message):
        """Send an error message"""
        message = f"❌ Sorry, I couldn't understand that. {error_message}"
        return self.send_message(to_number, message)
