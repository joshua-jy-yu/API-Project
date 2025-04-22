from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime, timedelta, timezone
import re

capitals = pd.read_csv("all_capital_timezones.csv")

app = Flask(__name__)
API_TOKEN = "supersecrettoken123"
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    capital = request.args.get('capital')
    if not capital:
        return jsonify({"error": "Missing 'capital' parameter"}), 400

    row = capitals[capitals["Capital"].str.lower() == capital.lower()]
    if row.empty:
        return jsonify({"error": f"Capital city '{capital}' not found"}), 404

    utc_offset_str = row.iloc[0]["UTC Offset"]

    # Parse the UTC offset into hours and minutes
    match = re.match(r'UTC([+-])(\d{2}):(\d{2})', utc_offset_str)
    if not match:
        return jsonify({"error": "Invalid UTC Offset format"}), 500

    sign, hours, minutes = match.groups()
    offset = timedelta(hours=int(hours), minutes=int(minutes))
    if sign == '-':
        offset = -offset

    # Calculate current local time
    utc_now = datetime.now(timezone.utc)
    local_time = utc_now + offset

    return jsonify({
        "capital": row.iloc[0]["Capital"],
        "utc_offset": utc_offset_str,
        "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S")
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
