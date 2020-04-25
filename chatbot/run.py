from subprocess import PIPE
import subprocess
import time
subprocess.Popen('rasa run actions', shell=True,
      stdin=PIPE)
print("Rasa action server running")
subprocess.Popen('rasa run -m models --enable-api --log-file out.log', shell=True,
      stdin=PIPE)
print("Rasa http api server running")