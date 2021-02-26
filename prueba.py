import os
import time
import sys
import psutil
import zipfile
import json
import subprocess
from subprocess import check_output

def get_service_pid(name):
    response = str(subprocess.check_output(f'tasklist /svc /FI "Services eq {name}"')).split('\\r\\n')
    for process in response:
        if name in process:
            pid = process.split()[1]
            return pid

def get_strings(PID):
    cmd = 'strings.exe -pid {PID} -raw -nh'
    strings = str(subprocess.check_output(cmd)).replace("\\\\","/")
    strings = list(set(strings.split("\\r\\n")))

    return strings

def a():
    return [proc.pid for proc in psutil.process_iter() if proc.name() == "csrss.exe"]
print(a())