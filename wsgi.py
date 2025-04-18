from flask import Flask
import streamlit.cli
import sys
import os

# Initialize Flask app
app = Flask(__name__)

# Proxy Streamlit through Flask
@app.route('/')
def run_streamlit():
    sys.argv = ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
    sys.exit(streamlit.cli.main())

# WSGI entry point
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)