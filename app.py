import time
import os
import socket
import subprocess
import psutil
import urllib.request
from flask import Flask, render_template, jsonify

app = Flask(__name__)


def get_stats():
    hostname = socket.gethostname()
    ip_address = subprocess.check_output(
        "hostname -I", shell=True
    ).decode().strip()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    uptime = f"{hours}h {minutes}m"

    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        internet = True
    except Exception:
        internet = False

    def status_for(value, warn, crit):
        if value < warn:
            return "green"
        elif value < crit:
            return "amber"
        else:
            return "red"

    return {
        "developer": "Sunka",
        "hostname": hostname,
        "ip_address": ip_address,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "internet": internet,
        "cpu_status": status_for(cpu_usage, 50, 80),
        "memory_status": status_for(memory_usage, 50, 80),
        "disk_status": status_for(disk_usage, 70, 90),
        "uptime": uptime,
    }


@app.route('/')
def system_status():
    return render_template("index.html", stats=get_stats())


@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# auto-trigger test on AWS
