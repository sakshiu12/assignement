from flask import Flask, render_template_string
import subprocess
import getpass
import datetime
import platform
import socket
import os

app = Flask(__name__)

@app.route('/htop')
def htop():
    # Get full name (replace with your actual name)
    full_name = "Your Full Name"  # REPLACE THIS WITH YOUR NAME
    
    # Get system username
    username = getpass.getuser()
    
    # Get server time in IST
    # Since pytz might not be available, using a fixed offset
    utc_time = datetime.datetime.utcnow()
    ist_offset = datetime.timedelta(hours=5, minutes=30)  # IST is UTC+5:30
    ist_time = utc_time + ist_offset
    server_time = ist_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Get a simplified top output that works on most systems
    try:
        if platform.system() == "Linux":
            top_output = subprocess.check_output(
                ['top', '-b', '-n', '1'], 
                universal_newlines=True,
                timeout=5  # Add timeout to prevent hanging
            )
        else:
            # Simplified system info for non-Linux systems
            top_output = "System Information:\n"
            top_output += f"System: {platform.system()}\n"
            top_output += f"Node: {platform.node()}\n"
            top_output += f"Release: {platform.release()}\n"
            top_output += f"Version: {platform.version()}\n"
            top_output += f"Machine: {platform.machine()}\n"
            top_output += f"Processor: {platform.processor()}\n"
            
            # Add memory info if on Linux
            if os.path.exists('/proc/meminfo'):
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = f.read()
                    top_output += "\nMemory Info:\n" + meminfo
                except:
                    top_output += "\nCould not read memory info."
    except Exception as e:
        top_output = f"Error getting system information: {str(e)}"
    
    # HTML template
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTOP Output</title>
        <style>
            body { font-family: monospace; margin: 20px; }
            pre { background-color: #f5f5f5; padding: 10px; overflow-x: auto; }
            .data-item { margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <div class="data-item">Name: {{ name }}</div>
        <div class="data-item">user: {{ username }}</div>
        <div class="data-item">Server Time (IST): {{ server_time }}</div>
        <div class="data-item">TOP output:</div>
        <pre>{{ top_output }}</pre>
    </body>
    </html>
    """
    
    return render_template_string(
        template,
        name=full_name,
        username=username,
        server_time=server_time,
        top_output=top_output
    )

if __name__ == '__main__':
    # Run on all network interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
