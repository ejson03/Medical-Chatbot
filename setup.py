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
process3 = subprocess.Popen(['python', 'app.py'], shell=True)

os.chdir(root+'/chatbot')
process1 = subprocess.Popen(['rasa', 'run', 'actions'], shell=True)

time.sleep(.300)
cmd = "rasa run -m models --endpoint endpoints.yml --enable-api --cors “*” --log-file out.log"
# process2 = subprocess.Popen(['rasa', 'run', '-m models', '--endpoint' , 'endpoints.yml', '--enable-api',
#                                 '--cors','--log-file',  'out.log'], shell=True)
process2 = subprocess.Popen(cmd, shell=True)
process2.wait()

os.kill(os.getid(process3.pid), SIGTERM)

