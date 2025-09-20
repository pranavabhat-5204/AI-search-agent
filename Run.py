from pyngrok import ngrok
import subprocess
import time

subprocess.Popen(["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"])

time.sleep(5)

public_url = ngrok.connect(8501)
print("Your Streamlit app is live at:", public_url)
