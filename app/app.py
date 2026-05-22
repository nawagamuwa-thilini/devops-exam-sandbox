import os
import base64
import json

from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host="localhost",
    port=6379,
    password=redis_password
)

@app.route("/process", methods=["POST"])
def process():

    if not request.is_json:
        return jsonify({"error": "Invalid request"}), 400

    payload = request.json.get("payload")

    if not payload:
        return jsonify({"error": "Payload required"}), 400

    try:
        decoded = base64.b64decode(payload)

        obj = json.loads(decoded.decode())

        return jsonify({
            "status": "processed",
            "result": obj
        })

    except Exception:
        return jsonify({
            "error": "Invalid payload"
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)