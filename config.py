import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Messaging Platform
    MESSAGING_PLATFORM = os.getenv('MESSAGING_PLATFORM', 'telegram').lower()
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Telegram Bot (FREE)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Twilio WhatsApp (PAID)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///reminders.db')
    
    # Timezone
    DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Asia/Kolkata')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        required = ['OPENAI_API_KEY']
        
        # Check messaging platform specific requirements
        platform = os.getenv('MESSAGING_PLATFORM', 'telegram').lower()
        
        if platform == 'telegram':
            if not os.getenv('TELEGRAM_BOT_TOKEN'):
                required.append('TELEGRAM_BOT_TOKEN')
        elif platform == 'whatsapp':
            required.extend(['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN'])
        
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
