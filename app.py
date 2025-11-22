from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from database import Database
from whatsapp_service import WhatsAppService
from task_parser import TaskParser
from scheduler import ReminderScheduler

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize services
database = Database()
whatsapp_service = WhatsAppService()
task_parser = TaskParser()
reminder_scheduler = ReminderScheduler(database, whatsapp_service)

# Start the background scheduler
reminder_scheduler.start()

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive messages from WhatsApp via Twilio
    
    Expected payload from Twilio:
    - From: User's WhatsApp number (format: whatsapp:+1234567890)
    - Body: Message text
    """
    try:
        # Get message data from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        if not incoming_msg or not from_number:
            return jsonify({"status": "error", "message": "Missing message or phone number"}), 400
        
        print(f"📨 Received message from {from_number}: {incoming_msg}")
        
        # Handle special commands
        if incoming_msg.lower() in ['help', 'start']:
            help_message = """👋 Welcome to WhatsApp Reminder Bot!

Send me a message like:
• "Remind me to buy petrol before Friday morning"
• "Remind me to call mom tomorrow at 6 PM"
• "Remind me to submit report on Thursday"

I'll understand when you want to be reminded and send you a notification at the right time!"""
            whatsapp_service.send_message(from_number, help_message)
            return jsonify({"status": "success"}), 200
        
        if incoming_msg.lower() == 'list':
            tasks = database.get_user_tasks(from_number)
            if not tasks:
                whatsapp_service.send_message(from_number, "📋 You have no pending reminders.")
            else:
                task_list = "📋 Your pending reminders:\n\n"
                for i, task in enumerate(tasks, 1):
                    task_list += f"{i}. {task.task_description}\n   ⏰ {task.reminder_time.strftime('%A, %B %d at %I:%M %p')}\n\n"
                whatsapp_service.send_message(from_number, task_list)
            return jsonify({"status": "success"}), 200
        
        # Parse the message to extract task and reminder time
        parsed_data = task_parser.parse_message(incoming_msg)
        
        if not parsed_data:
            # Try simple fallback parser
            parsed_data = task_parser.parse_simple_reminder(incoming_msg)
        
        if not parsed_data:
            error_msg = "I couldn't understand when you want to be reminded. Try something like: 'Remind me to [task] on [day] at [time]'"
            whatsapp_service.send_error(from_number, error_msg)
            return jsonify({"status": "error", "message": "Could not parse message"}), 200
        
        # Save the task to database
        task = database.add_task(
            user_phone=from_number,
            task_description=parsed_data['task_description'],
            reminder_time=parsed_data['reminder_time']
        )
        
        # Send confirmation to user
        reminder_time_str = parsed_data['reminder_time'].strftime('%A, %B %d at %I:%M %p')
        whatsapp_service.send_confirmation(
            from_number,
            parsed_data['task_description'],
            reminder_time_str
        )
        
        print(f"✅ Created task {task.id} for {from_number}")
        
        return jsonify({
            "status": "success",
            "task_id": task.id,
            "confidence": parsed_data.get('confidence', 'medium')
        }), 200
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        try:
            whatsapp_service.send_error(
                from_number,
                "An error occurred. Please try again."
            )
        except:
            pass
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    scheduler_status = reminder_scheduler.get_scheduler_status()
    return jsonify({
        "status": "healthy",
        "scheduler": scheduler_status
    }), 200


@app.route('/tasks/<phone>', methods=['GET'])
def get_tasks(phone):
    """Get all tasks for a user (for debugging/admin)"""
    try:
        # Ensure phone number format
        if not phone.startswith('whatsapp:'):
            phone = f'whatsapp:{phone}'
        
        include_sent = request.args.get('include_sent', 'false').lower() == 'true'
        tasks = database.get_user_tasks(phone, include_sent=include_sent)
        
        return jsonify({
            "status": "success",
            "tasks": [task.to_dict() for task in tasks]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "app": "WhatsApp Reminder Bot",
        "status": "running",
        "endpoints": {
            "webhook": "/webhook (POST) - Receive WhatsApp messages",
            "health": "/health (GET) - Health check",
            "tasks": "/tasks/<phone> (GET) - Get user tasks"
        }
    }), 200


if __name__ == '__main__':
    try:
        Config.validate()
        print("🚀 Starting WhatsApp Reminder Bot...")
        print(f"📱 Configured for WhatsApp number: {Config.TWILIO_WHATSAPP_NUMBER}")
        app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n⏹️ Shutting down...")
        reminder_scheduler.stop()
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        reminder_scheduler.stop()
