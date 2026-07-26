import time
import os
import socket
import subprocess
import psutil
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def system_status():
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
    uptime = f"{hours} Hours {minutes} Minutes"

    response = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1")
    if response == 0:
        internet = "Online ✅"
    else:
        internet = "Offline ❌"

    if cpu_usage < 50:
        cpu_status = "green"
    elif cpu_usage < 80:
        cpu_status = "orange"
    else:
        cpu_status = "red"

    if memory_usage < 50:
        memory_status = "green"
    elif memory_usage < 80:
        memory_status = "orange"
    else:
        memory_status = "red"

    if disk_usage < 70:
        disk_status = "green"
    elif disk_usage < 90:
        disk_status = "orange"
    else:
        disk_status = "red"

    return render_template(
        "index.html",
        developer="Sunka",
        hostname=hostname,
        ip_address=ip_address,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        disk_usage=disk_usage,
        internet=internet,
        cpu_status=cpu_status,
        memory_status=memory_status,
        uptime=uptime,
        disk_status=disk_status
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
