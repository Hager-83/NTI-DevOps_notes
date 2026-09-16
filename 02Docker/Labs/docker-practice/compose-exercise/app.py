import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


@app.route("/")
def home():
    count = r.incr("hits")
    return jsonify({
        "message": "Hello from the Compose exercise app!",
        "visit_count": count,
        "redis_host": redis_host,
    })


@app.route("/health")
def health():
    try:
        r.ping()
        redis_ok = True
    except Exception:
        redis_ok = False
    return jsonify({"app": "ok", "redis": redis_ok})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
