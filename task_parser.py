from datetime import datetime, timedelta
from typing import Optional, Dict
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dateutil import parser
import pytz
import re
from config import Config

class TaskParser:
    """Parse natural language messages to extract task information"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.timezone = pytz.timezone(Config.DEFAULT_TIMEZONE)
        
        # Prompt template for extracting task information
        self.prompt = PromptTemplate(
            input_variables=["message", "current_time"],
            template="""You are a helpful assistant that extracts task information from user messages.

Current date and time: {current_time}

User message: "{message}"

Extract the following information from the message:
1. Task description (what the user wants to be reminded about)
2. Reminder datetime (when to send the reminder, not the deadline)

Important rules:
- If the user says "before [day/time]", calculate an appropriate reminder time (e.g., "before Friday morning" -> Thursday 8 PM or Friday 6 AM)
- If the user says "on [day/time]", set the reminder for that exact time
- If no specific time is mentioned, use 9 AM as default
- Convert relative days (tomorrow, Friday, etc.) to actual dates
- The reminder time should be BEFORE the actual deadline/event

Return ONLY a JSON object with this exact format:
{{
    "task_description": "the task to remind about",
    "reminder_datetime": "YYYY-MM-DD HH:MM:SS",
    "confidence": "high/medium/low"
}}

Do not include any other text or explanation."""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def parse_message(self, message: str) -> Optional[Dict]:
        """
        Parse a message to extract task and reminder time
        
        Args:
            message: User's message text
        
        Returns:
            Dictionary with task_description and reminder_time, or None if parsing fails
        """
        try:
            # Get current time in the configured timezone
            current_time = datetime.now(self.timezone)
            current_time_str = current_time.strftime("%A, %B %d, %Y at %I:%M %p")
            
            # Use LangChain to extract information
            result = self.chain.invoke({
                "message": message,
                "current_time": current_time_str
            })
            
            # Parse the JSON response
            import json
            # Handle both dict and string responses
            if isinstance(result, dict):
                result = result.get('text', str(result))
            result = str(result).strip()
            # Remove markdown code blocks if present
            if result.startswith("```"):
                result = re.sub(r'```json\s*', '', result)
                result = re.sub(r'```\s*', '', result)
            
            parsed = json.loads(result)
            
            # Validate required fields
            if not parsed.get('task_description') or not parsed.get('reminder_datetime'):
                return None
            
            # Parse the datetime string
            reminder_time = parser.parse(parsed['reminder_datetime'])
            
            # Ensure the reminder time is timezone-aware
            if reminder_time.tzinfo is None:
                reminder_time = self.timezone.localize(reminder_time)
            
            # Ensure reminder time is in the future
            if reminder_time <= current_time:
                # If time is in the past, assume user meant next occurrence
                reminder_time = reminder_time + timedelta(days=1)
            
            return {
                'task_description': parsed['task_description'],
                'reminder_time': reminder_time,
                'confidence': parsed.get('confidence', 'medium')
            }
            
        except Exception as e:
            print(f"Error parsing message: {e}")
            return None
    
    def parse_simple_reminder(self, message: str) -> Optional[Dict]:
        """
        Fallback parser for simple reminders using pattern matching
        
        Args:
            message: User's message text
        
        Returns:
            Dictionary with task_description and reminder_time, or None
        """
        try:
            current_time = datetime.now(self.timezone)
            
            # Pattern: "remind me to [task] [time]"
            patterns = [
                r'remind me to (.+?) (tomorrow|today|tonight|in \d+ (hour|hours|day|days|minute|minutes))',
                r'remind me to (.+?)$',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, message.lower())
                if match:
                    task = match.group(1).strip()
                    
                    # Default to tomorrow at 9 AM
                    reminder_time = current_time + timedelta(days=1)
                    reminder_time = reminder_time.replace(hour=9, minute=0, second=0)
                    
                    return {
                        'task_description': task,
                        'reminder_time': reminder_time,
                        'confidence': 'low'
                    }
            
            return None
            
        except Exception as e:
            print(f"Error in simple parser: {e}")
            return None
