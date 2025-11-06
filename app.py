
import os
from flask import Flask, request, jsonify, render_template_string
from time import time
from collections import deque

app = Flask(__name__)

people = {}
events = deque(maxlen=1000)

def now():
    return time()

def ago(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    return f"{hours}h ago"

@app.post("/heartbeat")
def heartbeat():
    data = request.get_json(force=True, silent=True) or {}
    uid = data.get("user_id")
    name = data.get("name", "Anon")
    if not uid:
        return jsonify({"error": "missing user_id"}), 400
    people[uid] = {"name": name, "last": now()}
    return jsonify({"ok": True})

@app.post("/session/start")
def session_start():
    return heartbeat()

@app.post("/event")
def event():
    data = request.get_json(force=True, silent=True) or {}
    uid = data.get("user_id")
    name = data.get("name", "Anon")
    ts = float(data.get("ts", now()))
    ev = {
        "uid": uid or "unknown",
        "name": name,
        "ts": ts,
        "event": data.get("event", "activity"),
        "deck": data.get("deck"),
        "ease": data.get("ease"),
    }
    events.appendleft(ev)
    if uid:
        people[uid] = {"name": name, "last": ts}
    return jsonify({"ok": True})

@app.get("/feed.json")
def feed_json():
    t = now()
    online = [
        {"uid": uid, "name": p["name"], "last": p["last"], "ago": int(t - p["last"])}
        for uid, p in people.items()
        if t - p["last"] < 60
    ]
    return jsonify({"online": online, "events": list(events)})

@app.get("/")
def index():
    t = now()
    tpl = '''
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Friends Activity</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
    h1, h2 { margin: 0.5rem 0; }
    ul { padding-left: 1.2rem; }
    .pill { display:inline-block; padding: 2px 8px; border-radius: 999px; background: #eee; margin-left: 6px; font-size: 12px; }
    .muted { color: #666; }
  </style>
</head>
<body>
  <h1>Friends Activity</h1>

  <h2>Online now</h2>
  <ul>
  {% for uid, p in online %}
      <li>{{ p["name"] }} <span class="pill">active {{ p["ago"] }}</span></li>
  {% else %}
      <li>Nobody online.</li>
  {% endfor %}
  </ul>

  <h2>Recent activity</h2>
  <ul>
  {% for e in events %}
      <li><strong>{{ e["name"] }}</strong> answered a card{% if e["deck"] %} in <em>{{ e["deck"] }}</em>{% endif %}{% if e["ease"] is not none %} (ease={{ e["ease"] }}){% endif %} <span class="muted">{{ e["ago"] }}</span></li>
  {% else %}
      <li>No activity yet.</li>
  {% endfor %}
  </ul>
</body>
</html>
'''
    online_pairs = []
    for uid, p in list(people.items()):
        dt = t - p["last"]
        if dt < 3600 * 12:
            online_pairs.append((uid, {"name": p["name"], "ago": ago(dt)}))
    evs = []
    for e in list(events):
        evs.append({**e, "ago": ago(t - e["ts"])})
    return render_template_string(tpl, online=online_pairs, events=evs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
