import csv
import inspect
import os
import sys
import time


def print_cpu_usage():
    cpu_pct = str(round(
        float(os.popen(
            '''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),
        2))
    print("CPU Usage: " + cpu_pct)
    return cpu_pct


def print_mem_usage():
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    result = round((used_memory / total_memory) * 100, 2)
    print("RAM memory % used:", result)
    return result


def print_open_fds():
    frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[1]
    fds = set(os.listdir('/proc/self/fd/'))
    print("{}:{} count of file descriptors: {}".format(filename, line_number, len(fds)))
    return len(fds)


if __name__ == '__main__':
    while True:
        with open('names.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow({print_cpu_usage(), print_mem_usage(), print_open_fds()})
        # User must write number of seconds
        time.sleep(float(sys.argv[1]))
