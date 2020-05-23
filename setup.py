import os
import subprocess
import time
from psutil import process_iter
from signal import SIGTERM
from dotenv import load_dotenv
from termcolor import colored
from concurrent.futures import ProcessPoolExecutor

root = os.path.abspath(os.getcwd())


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


def execute(cmd, path=None):
    if path!= None:
        os.chdir(root+ path)

    process = subprocess.Popen(cmd, shell=True)

if __name__ == "__main__":
    killProcesses()
    load_dotenv()
    print(colored("Kill all processes", "magenta"))
    cmd = "rasa run -m models --endpoint endpoints.yml --credentials credentials.yml --enable-api --cors “*”"
    app = os.path.join(root, 'flask-app', 'app.py')
    execute(['rasa', 'run', 'actions'], '/chatbot')
    execute(cmd, '/chatbot')
    execute( ['python', app])






