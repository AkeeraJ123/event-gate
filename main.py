import time
import threading
from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

STATE = {
"eth": 0,
"base": 0,
"polygon": 0,
"started_at": time.time(),
"events_total": 0
}

PRICE_PER_EVENT = 0.001
EXTERNAL_PRICE = 0.01


def event_engine():
while True:
time.sleep(5)

STATE["eth"] += 1
STATE["base"] += 1
STATE["polygon"] += 1
STATE["events_total"] += 3

print(
"EVENT_TICK",
{
"eth": STATE["eth"],
"base": STATE["base"],
"polygon": STATE["polygon"],
"events_total": STATE["events_total"]
}
)


DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Event Gate — Live</title>
<style>
body {
background:#0b0b0b;
color:#00ff88;
font-family: monospace;
padding:30px;
}
.card {
border:1px solid #00ff88;
padding:20px;
margin-bottom:15px;
border-radius:8px;
}
</style>
</head>
<body>

<h1>⚡ EVENT GATE — LIVE</h1>

<div class="card">ETH Events: {{eth}}</div>
<div class="card">BASE Events: {{base}}</div>
<div class="card">POLYGON Events: {{polygon}}</div>
<div class="card">TOTAL Events: {{total}}</div>
<div class="card">Uptime: {{uptime}} seconds</div>
<div class="card">Internal Cost: ${{cost}}</div>
<div class="card">Revenue Potential: ${{revenue}}</div>

</body>
</html>
"""


@app.route("/")
def dashboard():
uptime = int(time.time() - STATE["started_at"])
cost = round(STATE["events_total"] * PRICE_PER_EVENT, 4)
revenue = round(STATE["events_total"] * EXTERNAL_PRICE, 2)

return render_template_string(
DASHBOARD_HTML,
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
t = threading.Thread(target=event_engine, daemon=True)
t.start()

port = int(os.environ.get("PORT", 8000))
app.run(host="0.0.0.0", port=port)

