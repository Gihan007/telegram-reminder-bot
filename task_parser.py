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
2. Reminder datetime (when to send the reminder)

Important rules:
- "in X seconds/minutes/hours" means ADD that time to current time
- "within X seconds/minutes/hours" means ADD that time to current time
- "after X seconds/minutes/hours" means ADD that time to current time
- "tomorrow" means next day at 9 AM unless time specified
- "tonight" means today at 8 PM
- "today" means today, preserve current time or add specified time
- If no specific time mentioned, use 9 AM as default for future days
- Calculate from the CURRENT time provided above

Examples:
- "in 30 seconds" from 2:21 PM -> 2:21:30 PM today
- "within 2 minutes" from 2:21 PM -> 2:23 PM today
- "in 1 hour" from 2:21 PM -> 3:21 PM today
- "tomorrow at 3pm" -> tomorrow at 3:00 PM

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
        # First try the simple parser for common patterns (faster and more reliable)
        simple_result = self.parse_simple_reminder(message)
        if simple_result and simple_result.get('confidence') == 'high':
            return simple_result
        
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
            message_lower = message.lower()
            
            # Extract task description (everything before time indicators)
            task_match = re.search(r'remind me to (.+?)(?:\s+in\s+|\s+within\s+|\s+after\s+|$)', message_lower)
            if not task_match:
                return None
            
            task = task_match.group(1).strip()
            reminder_time = current_time
            
            # Parse relative time: "in/within/after X seconds/minutes/hours/days"
            time_match = re.search(r'(?:in|within|after)\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours|day|days)', message_lower)
            
            if time_match:
                amount = int(time_match.group(1))
                unit = time_match.group(2)
                
                if 'second' in unit:
                    reminder_time = current_time + timedelta(seconds=amount)
                elif 'minute' in unit:
                    reminder_time = current_time + timedelta(minutes=amount)
                elif 'hour' in unit:
                    reminder_time = current_time + timedelta(hours=amount)
                elif 'day' in unit:
                    reminder_time = current_time + timedelta(days=amount)
                
                return {
                    'task_description': task,
                    'reminder_time': reminder_time,
                    'confidence': 'high'
                }
            
            # Parse specific times: "tomorrow", "today", "tonight"
            if 'tomorrow' in message_lower:
                reminder_time = current_time + timedelta(days=1)
                reminder_time = reminder_time.replace(hour=9, minute=0, second=0)
            elif 'tonight' in message_lower:
                reminder_time = current_time.replace(hour=20, minute=0, second=0)
            elif 'today' in message_lower:
                reminder_time = current_time.replace(hour=18, minute=0, second=0)
            else:
                # Default to tomorrow at 9 AM
                reminder_time = current_time + timedelta(days=1)
                reminder_time = reminder_time.replace(hour=9, minute=0, second=0)
            
            return {
                'task_description': task,
                'reminder_time': reminder_time,
                'confidence': 'medium'
            }
            
        except Exception as e:
            print(f"Error in simple parser: {e}")
            return None
