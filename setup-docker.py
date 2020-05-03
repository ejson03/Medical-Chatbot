import os
import subprocess
import time
from psutil import process_iter
from signal import SIGTERM

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


root = os.path.abspath(os.getcwd())

os.chdir(root+'/flask-app')
process1 = subprocess.Popen(['python3', 'app.py'], preexec_fn=os.setsid)

os.chdir(root+'/chatbot')
process2 = subprocess.Popen(['rasa', 'run', 'actions'], preexec_fn=os.setsid)

time.sleep(.300)
process3 = subprocess.Popen(['rasa', 'run', '-m models', '--endpoint' , 'endpoints.yml', '--credential', 'credentials.yml',
                                 '--enable-api', '--log-file',  'out.log'], preexec_fn=os.setsid)
process3.wait()

os.killpg(os.getpgid(process1.pid), SIGTERM)



