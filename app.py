import os
import socket

import redis
from flask import Flask, request

app = Flask(__name__)

STUDENT = os.getenv("STUDENT", "unknown")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


def get_redis():
    return redis.Redis(
        host=REDIS_HOST,
        port=6379,
        password=REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=3,
    )


@app.route("/health")
def health():
    return "ok"


@app.route("/")
def index():
    r = get_redis()
    hits = r.incr("hits")
    hostname = socket.gethostname()
    return f"KR2 | {STUDENT} | container {hostname} | hits: {hits}"


@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto", "none")
    client = request.headers.get("X-Real-IP", "none")
    host = request.headers.get("Host", "none")
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
