import os
import subprocess
import signal

def application(environ, start_response):
    # This is just a placeholder - Streamlit will run separately
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Streamlit app is running']

# Start Streamlit process when WSGI app loads
if __name__ == '__main__':
    streamlit_process = subprocess.Popen(['streamlit', 'run', 'main.py', '--server.port=8080', 
                                          '--server.address=0.0.0.0', '--server.headless=true', 
                                          '--server.enableCORS=false', '--server.enableXsrfProtection=false'])
    
    def handle_sigterm(signo, frame):
        if streamlit_process:
            streamlit_process.terminate()
        exit(0)
        
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.pause()