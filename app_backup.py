import subprocess
import os
import socket
import psutil
from flask import Flask, jsonify

# Create the web application
app = Flask(__name__)

# Tell the app what to do when someone visits the root webpage ('/')
@app.route('/')
def system_status():
    # 1. Gather all the data
    hostname = socket.gethostname()
    ip_address = subprocess.check_output(
    "hostname -I", shell=True
).decode().strip()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # 2. Check the network
    response = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1")
    if response == 0:
        internet = "Online ✅"
    else:
        internet = "Offline ❌"

    # 3. Return the data to the web browser in JSON format
    return jsonify({
        "Developer": "Sunka",
        "Hostname": hostname,
        "IP Address": ip_address,
        "CPU Usage": f"{cpu_usage} %",
        "Memory Usage": f"{memory_usage} %",
        "Disk Usage": f"{disk_usage} %",
        "Internet": internet
    })

# Start the web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
