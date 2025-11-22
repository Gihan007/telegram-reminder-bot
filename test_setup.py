"""
Test script to verify WhatsApp bot setup and functionality
Run this after setting up your .env file
"""

import os
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    load_dotenv()
    
    required_vars = [
        'OPENAI_API_KEY',
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER'
    ]
    
    print("🔍 Checking environment variables...\n")
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'TOKEN' in var:
                display = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display = value
            print(f"✅ {var}: {display}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    return all_set

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🧪 Testing OpenAI connection...\n")
    
    try:
        from langchain_openai import ChatOpenAI
        from config import Config
        
        llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        response = llm.invoke("Say 'Hello' in one word")
        print(f"✅ OpenAI connection successful!")
        print(f"   Response: {response.content}\n")
        return True
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}\n")
        return False

def test_twilio_connection():
    """Test Twilio API connection"""
    print("🧪 Testing Twilio connection...\n")
    
    try:
        from twilio.rest import Client
        from config import Config
        
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        
        # Get account info
        account = client.api.accounts(Config.TWILIO_ACCOUNT_SID).fetch()
        print(f"✅ Twilio connection successful!")
        print(f"   Account: {account.friendly_name}")
        print(f"   Status: {account.status}\n")
        return True
    except Exception as e:
        print(f"❌ Twilio connection failed: {e}\n")
        return False

def test_database():
    """Test database creation and operations"""
    print("🧪 Testing database...\n")
    
    try:
        from database import Database
        from datetime import datetime, timedelta
        
        db = Database()
        
        # Add test task
        test_task = db.add_task(
            user_phone="whatsapp:+1234567890",
            task_description="Test reminder",
            reminder_time=datetime.now() + timedelta(hours=1)
        )
        
        print(f"✅ Database working!")
        print(f"   Created test task ID: {test_task.id}\n")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("WhatsApp Reminder Bot - Setup Verification")
    print("=" * 50 + "\n")
    
    env_ok = check_environment()
    
    if not env_ok:
        print("\n⚠️  Please set all required environment variables in .env file")
        print("   Copy .env.example to .env and fill in your credentials\n")
        return
    
    print("\n" + "=" * 50)
    
    openai_ok = test_openai_connection()
    twilio_ok = test_twilio_connection()
    db_ok = test_database()
    
    print("=" * 50)
    print("\n📊 Test Summary:")
    print(f"   Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"   OpenAI Connection: {'✅' if openai_ok else '❌'}")
    print(f"   Twilio Connection: {'✅' if twilio_ok else '❌'}")
    print(f"   Database: {'✅' if db_ok else '❌'}")
    
    if all([env_ok, openai_ok, twilio_ok, db_ok]):
        print("\n🎉 All tests passed! You're ready to run the bot.")
        print("   Run: python app.py\n")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.\n")

if __name__ == "__main__":
    main()
