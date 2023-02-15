import subprocess
import time
import sys 
script_path = '/Users/javier/GIT/fala/tayloy/as.py'
script_arg = "0"

term = subprocess.Popen(['open', '-a', 'Terminal'])
term.communicate("python3 /Users/javier/GIT/fala/tayloy/as.py 0")