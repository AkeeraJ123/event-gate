import os
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# ---- GLOBAL STATE ----
stats = {
"eth": 0,
"base": 0,
"polygon": 0,
"started_at": int(time.time())
}

# ---- EVENT LOOP (AUTOMATIC) ----
def event_loop():
while True:
stats["eth"] += 1
stats["base"] += 2
stats["polygon"] += 3
time.sleep(2)

# Start background event engine
threading.Thread(target=event_loop, daemon=True).start()

# ---- API ----
@app.route("/")
def dashboard():
return f"""
<html>
<head>
<title>Event Gate — Live</title>
<meta http-equiv="refresh" content="5">
<style>
body {{
font-family: monospace;
background: #0e0e11;
color: #00ffcc;
padding: 40px;
}}
h1 {{ color: #ffffff; }}
.box {{
background: #15151c;
padding: 20px;
border-radius: 12px;
width: 300px;
}}
</style>
</head>
<body>
<h1>⚡ Event Gate — Live</h1>
<div class="box">
<p>ETH events: {stats["eth"]}</p>
<p>Base events: {stats["base"]}</p>
<p>Polygon events: {stats["polygon"]}</p>
<p>Uptime: {int(time.time()) - stats["started_at"]}s</p>
</div>
</body>
</html>
"""

@app.route("/stats")
def get_stats():
return jsonify(stats)

# ---- ENTRYPOINT ----
if __name__ == "__main__":
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
