
from flask import Flask, request
from flask_cors import CORS
import requests, json
from pymongo import MongoClient
from datetime import datetime
import pytz,os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
mongo_url = os.getenv("MONGO_URL")
# MongoDB connection
client = MongoClient(mongo_url)
db = client['STORING_KEYS']
collection = db['tele_bot_1']

# Get bot credentials
document = collection.find_one({'TELEGRAM_BOT_UNAME': 'user_info_b_1_bot'})
TELEGRAM_BOT_TOKEN = document['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = document['TELEGRAM_CHAT_ID']

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

@app.route("/", methods=['GET'])
def home_route():
    return "The Backend working fine"

@app.route('/testing-stage-url', methods=['GET'])
def notify_telegram():
    ip = request.remote_addr
    send_telegram_message(f"🔔 Webhook triggered from IP: {ip}")
    return "You have triggered a notification to Telegram!"

@app.route('/report-error', methods=['POST'])
def report_error():
    data = request.get_json()
    error_msg = data.get('error', '❗ Error field missing in payload')

    # Get current time in IST
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')

    # Format and send message
    message = f"🚨 Error Reported:\n{error_msg}\n🕒 Time (IST): {current_time}"
    send_telegram_message(message)

    return {"status": "sent", "message": error_msg, "timestamp": current_time}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
