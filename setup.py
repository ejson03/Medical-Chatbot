import os
import subprocess
import time
from psutil import process_iter
from signal import SIGTERM
from dotenv import load_dotenv

def killProcesses():
    try:
        for proc in process_iter():
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == 5055:
                    proc.send_signal(SIGTERM)
                if conns.laddr.port == 5000:
                    proc.send_signal(SIGTERM) 
                if conns.laddr.port == 5005:
                    proc.send_signal(SIGTERM)
    except:
        print('oopps')

killProcesses()

load_dotenv()
root = os.path.abspath(os.getcwd())

os.chdir(root+ '/flask-app')
app = os.path.join(root, 'flask-app', 'app.py')
process3 = subprocess.Popen(['python', app], shell=True)

os.chdir(root+'/chatbot')
process1 = subprocess.Popen(['rasa', 'run', 'actions'], shell=True)

time.sleep(.300)
cmd = "rasa run -m models --endpoint endpoints.yml --enable-api --cors “*” --log-file out.log"
process2 = subprocess.Popen(cmd, shell=True)
process2.wait()

os.kill(os.getid(process.pid), SIGTERM)

