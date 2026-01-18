import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

STATE = {
    "eth": 0,
    "base": 0,
    "polygon": 0,
    "started_at": time.time()
}

EVENT_PRICE = 0.001  # what YOU charge per event ($)

def event_loop():
    while True:
        STATE["eth"] += 1
        STATE["base"] += 1
        STATE["polygon"] += 1
        print("EVENT TICK:", STATE)
        time.sleep(5)  # every 5 seconds (adjust later)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            total = STATE["eth"] + STATE["base"] + STATE["polygon"]
            revenue = total * EVENT_PRICE

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "chains": STATE,
                "total_events": total,
                "revenue_usd": round(revenue, 2),
                "uptime_minutes": int((time.time() - STATE["started_at"]) / 60),
                "status": "live"
            }, indent=2).encode())

def run_server():
    port = 8080
    server = HTTPServer(("", port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=event_loop, daemon=True).start()
    run_server()
