"""Clean up old test data"""
from database import Database, Task

db = Database()
session = db.get_session()
try:
    # Delete test data
    deleted = session.query(Task).filter(
        Task.user_phone.in_(['test_user', 'whatsapp:+1234567890'])
    ).delete(synchronize_session=False)
    session.commit()
    print(f'✅ Cleaned {deleted} old test records')
finally:
    session.close()
