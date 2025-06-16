from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data_store.json'

# Ensure the file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/save-url', methods=['POST'])
def save_url():
    data = request.get_json()
    url = data.get('url')
    timestamp = data.get('time_stamp')

    if not url or not timestamp:
        return {"error": "Missing 'url' or 'time_stamp' in request"}, 400

    entry = {
        "url": url,
        "time_stamp": timestamp
    }

    try:
        with open(DATA_FILE, 'r+') as f:
            existing_data = json.load(f)
            existing_data.append(entry)
            f.seek(0)
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        return {"error": str(e)}, 500

    return {"status": "success", "message": "Data saved"}, 200

@app.route('/get-urls', methods=['GET'])
def get_urls():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
