from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()

class Task(Base):
    """Task model for storing reminders"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_phone = Column(String(20), nullable=False)
    task_description = Column(String(500), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Task(id={self.id}, user={self.user_phone}, task={self.task_description[:30]})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_phone': self.user_phone,
            'task_description': self.task_description,
            'reminder_time': self.reminder_time.isoformat(),
            'created_at': self.created_at.isoformat(),
            'is_sent': self.is_sent,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }


class Database:
    """Database manager"""
    
    def __init__(self, database_url=None):
        self.database_url = database_url or Config.DATABASE_URL
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    def add_task(self, user_phone, task_description, reminder_time):
        """Add a new task to the database"""
        session = self.get_session()
        try:
            task = Task(
                user_phone=user_phone,
                task_description=task_description,
                reminder_time=reminder_time
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        finally:
            session.close()
    
    def get_pending_reminders(self, current_time):
        """Get all pending reminders that should be sent"""
        session = self.get_session()
        try:
            tasks = session.query(Task).filter(
                Task.is_sent == False,
                Task.reminder_time <= current_time
            ).all()
            return tasks
        finally:
            session.close()
    
    def mark_task_sent(self, task_id):
        """Mark a task as sent"""
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                task.is_sent = True
                task.sent_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_user_tasks(self, user_phone, include_sent=False):
        """Get all tasks for a specific user"""
        session = self.get_session()
        try:
            query = session.query(Task).filter(Task.user_phone == user_phone)
            if not include_sent:
                query = query.filter(Task.is_sent == False)
            return query.order_by(Task.reminder_time).all()
        finally:
            session.close()
