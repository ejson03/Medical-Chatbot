import os
import subprocess
import time
from psutil import process_iter
from signal import SIGTERM
from dotenv import load_dotenv
from termcolor import colored


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
print(colored("Kill all processes", "magenta"))

load_dotenv()
root = os.path.abspath(os.getcwd())

os.chdir(root+'/chatbot')
process1 = subprocess.Popen(['rasa', 'run', 'actions'], shell=True)

cmd = "rasa run -m models --endpoint endpoints.yml --enable-api --cors “*” --log-file out.log"
process2 = subprocess.Popen(cmd, shell=True)


time.sleep(.300)
app = os.path.join(root, 'flask-app', 'app.py')
process3 = subprocess.Popen(['python', app], shell=True)
process3.wait()





