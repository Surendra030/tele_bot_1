
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage (resets on restart)
data_store = []

@app.route('/', methods=['GET'])
def home():
    return {"message": "Backend Server Working.."}, 200

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
    data = []
    data_store.append(entry)
    return {"status": "success", "message": "Data saved"}, 200

@app.route('/get-urls', methods=['GET'])
def get_urls():
    obj = [data_store[-1]
    return jsonify(obj), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
