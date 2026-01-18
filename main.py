import os
import time
import threading
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# --- GLOBAL STATE ---
stats = {
"eth": 0,
"base": 0,
"polygon": 0,
"started_at": int(time.time())
}

# --- EVENT LOOP (AUTOMATIC) ---
def event_loop():
while True:
stats["eth"] += 1
stats["base"] += 1
stats["polygon"] += 1
time.sleep(5) # event tick every 5 seconds

# --- START BACKGROUND WORKER ---
threading.Thread(target=event_loop, daemon=True).start()

# --- DASHBOARD UI ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Event Gate — Live</title>
<style>
body {
background: #0b0f14;
color: #e5e7eb;
font-family: monospace;
padding: 40px;
}
.card {
background: #111827;
border-radius: 12px;
padding: 20px;
margin-bottom: 20px;
box-shadow: 0 0 20px rgba(0,255,255,0.1);
}
h1 { color: #38bdf8; }
.stat { font-size: 24px; }
</style>
</head>
<body>
<h1>⚡ Event Gate — Live Dashboard</h1>

<div class="card">
<div class="stat">ETH Events: {{ eth }}</div>
<div class="stat">BASE Events: {{ base }}</div>
<div class="stat">POLYGON Events: {{ polygon }}</div>
</div>

<div class="card">
Started at: {{ started_at }}
</div>

<script>
setTimeout(() => location.reload(), 5000);
</script>
</body>
</html>
"""

@app.route("/")
def dashboard():
return render_template_string(
DASHBOARD_HTML,
eth=stats["eth"],
base=stats["base"],
polygon=stats["polygon"],
started_at=stats["started_at"]
)

@app.route("/health")
def health():
return jsonify({"status": "ok", "stats": stats})

# --- RAILWAY ENTRYPOINT ---
if __name__ == "__main__":
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
