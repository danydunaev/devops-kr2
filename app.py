import os
import redis
from flask import Flask, request

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", None)

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

@app.route("/")
def index():
    hits = r.incr("hits")
    hostname = os.uname().nodename
    return f"KR2 | DUNAEV | container {hostname} | hits: {hits}\n"

@app.route("/health")
def health():
    return "ok\n"

@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto", "none")
    client = request.headers.get("X-Real-IP", "none")
    host = request.headers.get("Host", "none")
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"
