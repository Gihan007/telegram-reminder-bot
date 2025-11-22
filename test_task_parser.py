import pytest
from datetime import datetime, timedelta
from task_parser import TaskParser
import pytz

@pytest.fixture
def parser():
    """Create a TaskParser instance for testing"""
    return TaskParser()

def test_parse_simple_reminder(parser):
    """Test parsing a simple reminder message"""
    message = "Remind me to buy milk tomorrow at 9 AM"
    result = parser.parse_message(message)
    
    assert result is not None
    assert "buy milk" in result['task_description'].lower()
    assert isinstance(result['reminder_time'], datetime)

def test_parse_before_deadline(parser):
    """Test parsing 'before' time expressions"""
    message = "Remind me to submit report before Friday morning"
    result = parser.parse_message(message)
    
    assert result is not None
    assert "report" in result['task_description'].lower()

def test_fallback_parser(parser):
    """Test fallback parser for simple patterns"""
    message = "remind me to call John"
    result = parser.parse_simple_reminder(message)
    
    assert result is not None
    assert "call john" in result['task_description'].lower()
    assert result['confidence'] == 'low'

def test_timezone_awareness(parser):
    """Ensure parsed times are timezone-aware"""
    message = "Remind me to workout tomorrow"
    result = parser.parse_message(message)
    
    if result:
        assert result['reminder_time'].tzinfo is not None
