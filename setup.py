import os, sys
import subprocess
import time
from psutil import process_iter
from signal import SIGTERM
from concurrent.futures import ProcessPoolExecutor

root = os.path.abspath(os.getcwd())

def killProcesses():
    try:
        for proc in process_iter():
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == 5055:
                    print("Killed action server")
                    proc.send_signal(SIGTERM)
                if conns.laddr.port == 5000:
                    print("Killed main server")
                    proc.send_signal(SIGTERM) 
                if conns.laddr.port == 5005:
                    print("Killed rasa server")
                    proc.send_signal(SIGTERM)
    except:
        print('Processes not killed')


def execute(cmd, path=None):
    print(cmd)
    if path!= None:
        os.chdir(root+ path)
    else: 
        os.chdir(root)

    #process = subprocess.Popen(cmd, shell=True)
    os.system(cmd)

if __name__ == "__main__":
    try:
        killProcesses()
        cmd = "rasa run -m models --endpoint endpoints.yml --credentials credentials.yml --enable-api --debug --cors “*”"
        execute("rasa run actions", '/actions')
        execute(cmd, '/chatbot')
        execute("npm start")
    except KeyboardInterrupt:
        killProcesses()
        sys.exit()