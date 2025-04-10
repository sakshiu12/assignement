from flask import Flask, render_template_string
import os
import subprocess
import getpass
import datetime
import pytz

app = Flask(__name__)

@app.route('/htop')
def htop():
    # Get full name (you should replace this with your actual name)
    full_name = "Your Full Name"  # Replace with your name
    
    # Get system username
    username = getpass.getuser()
    
    # Get server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Get top output
    try:
        top_output = subprocess.check_output(
            ['top', '-b', '-n', '1'], 
            universal_newlines=True
        )
    except Exception as e:
        top_output = f"Error getting top output: {str(e)}"
    
    # HTML template for the page
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
    # Run the application on a specific port with public visibility
    app.run(host='0.0.0.0', port=5000, debug=True)
