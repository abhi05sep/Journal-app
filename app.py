from flask import Flask, render_template, request, redirect, url_for
import json
import os
import time

app = Flask(__name__)

# -----------------------------
# Persistent storage (existing app)
# -----------------------------
DATA_FILE = '/data/entries.json'


def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_entries(entries):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f)


# -----------------------------
# Startup delay (screenshot code)
# -----------------------------
STARTUP_DELAY_SECONDS = 5
ready_at = time.time() + STARTUP_DELAY_SECONDS


# -----------------------------
# Main UI routes
# -----------------------------
@app.route('/')
def index():
    entries = load_entries()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    entry = request.form.get('entry')
    if entry:
        entries = load_entries()
        entries.append(entry)
        save_entries(entries)
    return redirect(url_for('index'))


# -----------------------------
# Kubernetes probes (screenshot code)
# -----------------------------

# Liveness probe
@app.route('/healthz')
def healthz():
    return "ok", 200


# Readiness probe
@app.route('/readyz')
def readyz():
    if time.time() < ready_at:
        return "warming up", 503
    return "ready", 200


# -----------------------------
# App start
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

