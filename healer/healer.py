# Python script for the healer daemon

from subprocess import check_output
import subprocess

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
    mem_usage = get_memory_usage_for_pid(pid)
    cpu_percent_usage = get_cpu_usage_for_pid(pid)
    print "Name\t PID\t  FD-Used\t MemUsed\t %CPU\t"
    print name, "\t", pid,"\t\t", fd_usage,"\t", mem_usage,"\t", cpu_percent_usage
    

if __name__ == '__main__':
    import time

    print('Starting up ...')
    #time.sleep(10)
    print('Startup complete')

    while True:
        pid_list = []
        pid_name = 'httpd'
        pidstr = get_pid(pid_name)
        pid_list = pidstr.split()
        print pid_list
        for pid in pid_list:
            print pid
            get_metrics(pid_name, pid)
        
        time.sleep(50)
