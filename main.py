import time
import threading
from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

STATE = {
"eth": 0,
"base": 0,
"polygon": 0,
"events_total": 0,
"started_at": time.time()
}

PRICE_INTERNAL = 0.001
PRICE_EXTERNAL = 0.01


def tick():
STATE["eth"] += 1
STATE["base"] += 1
STATE["polygon"] += 1
STATE["events_total"] += 3
print("EVENT_TICK", STATE)


def engine_loop():
while True:
time.sleep(5)
tick()


@app.route("/")
def dashboard():
uptime = int(time.time() - STATE["started_at"])
cost = round(STATE["events_total"] * PRICE_INTERNAL, 4)
revenue = round(STATE["events_total"] * PRICE_EXTERNAL, 2)

return render_template_string("""
<html>
<head>
<title>Event Gate — Live</title>
<style>
body { background:#0b0b0b; color:#00ff88; font-family:monospace; padding:40px; }
.card { border:1px solid #00ff88; padding:15px; margin-bottom:10px; }
</style>
</head>
<body>
<h1>⚡ EVENT GATE — LIVE</h1>
<div class="card">ETH: {{eth}}</div>
<div class="card">BASE: {{base}}</div>
<div class="card">POLYGON: {{polygon}}</div>
<div class="card">TOTAL EVENTS: {{total}}</div>
<div class="card">UPTIME: {{uptime}}s</div>
<div class="card">INTERNAL COST: ${{cost}}</div>
<div class="card">REVENUE POTENTIAL: ${{revenue}}</div>
</body>
</html>
""",
eth=STATE["eth"],
base=STATE["base"],
polygon=STATE["polygon"],
total=STATE["events_total"],
uptime=uptime,
cost=cost,
revenue=revenue
)


@app.route("/metrics")
def metrics():
return jsonify(STATE)


if __name__ == "__main__":
t = threading.Thread(target=engine_loop)
t.daemon = True
t.start()

port = int(os.environ.get("PORT", 8000))
app.run(host="0.0.0.0", port=port)

