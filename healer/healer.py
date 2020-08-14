# Python script for the healer daemon

from subprocess import check_output
import subprocess
import json
import time
import os

METRICS_FILE = "/var/log/metrics.log"
ALERTS_FILE = "/var/log/alerts.log"
FD_THRESHOLD = 100

def remove_log_files():
    check_output(['rm', '-f', METRICS_FILE])
    check_output(['rm', '-f', ALERTS_FILE])

def get_pid(process_name):
    return check_output(["pidof",process_name])

def get_open_fd_for_pid(pid):
    cmd = "ls -l /proc/" + str(pid) + "/fd | wc -l"
    p = subprocess.Popen(cmd, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    result = p.communicate()[0]
    return result.strip()

def get_memory_usage_for_pid(pid):
    cmd = "pmap " + pid
    p = subprocess.Popen(cmd, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    result = p.communicate()[0]
    mem_usage_str = result.split()
    return mem_usage_str[-1].strip()

def get_cpu_usage_for_pid(pid):
    cmd = "ps -p " + pid + " -o %cpu"
    p = subprocess.Popen(cmd, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    result = p.communicate()[0]
    return (result.split()[1]).strip()


def get_metrics(name=None, pid=None):
    if pid is None or pid == 0:
        return
    fd_usage = get_open_fd_for_pid(pid)
    data = {}
    data['timestamp'] = time.time()
    data['pid'] = pid 
    data['proc_name'] = name

    if int(fd_usage) > FD_THRESHOLD:
        data['severity'] = 'CRITICAL'
        data['message'] = 'FD value exceeding threshold'
    else:
        data['severity'] = 'INFO'
        data['message'] = 'FD value conformant'

    data['alert_type'] = 'fd'
    data['fd_used'] = fd_usage
    data['threshold'] = FD_THRESHOLD
    json_data = json.dumps(data)
    json_data = json_data + "\n"
    f = open(ALERTS_FILE, "a")
    f.write(json_data)
    f.close()

    mem_usage = get_memory_usage_for_pid(pid)
    cpu_percent_usage = get_cpu_usage_for_pid(pid)
  
    data = {}
    data['timestamp'] = time.time()
    data['pid'] = pid
    data['proc_name'] = name
    data['fd_used'] = fd_usage
    data['mem_usage'] = mem_usage
    data['cpu_percent_usage'] = cpu_percent_usage
    json_data = json.dumps(data)
    f = open(METRICS_FILE, "a")
    f.write(json_data)
    f.write("\n")
    f.close()

    

if __name__ == '__main__':

    print('Starting up ...')
    time.sleep(10)
    print('Startup complete')
    remove_log_files()

    while True:
        pid_list = []
        pid_name = 'httpd'
        pidstr = get_pid(pid_name)
        pid_list = pidstr.split()
        for pid in pid_list:
            get_metrics(pid_name, pid)
        
        time.sleep(30)
