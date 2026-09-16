from flask import Flask, jsonify
import platform
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from the Python app!",
        "python_version": platform.python_version(),
        "hostname": platform.node(),
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
