from os import listdir
from os.path import isfile, isdir, join

from eventlog import *
from btracelog import *

class Info:
    def __init__(self):
        self.application_id = None
        self.configuration_id = None
        self.application_name = None
        self.input_size = None

        self.running_time = None
        self.gc_overhead = None
        self.avg_cpu_usage = None
        self.max_peak_memory = None

    def __repr__(self):
        result = ""
        result += "application_id = " + str(self.application_id) + "\n"
        result += "configuation_id = " + str(self.configuration_id) + "\n"
        result += "application_name = " + str(self.application_name) + "\n"
        result += "input_size = " + str(self.input_size) + "\n"
        result += "running_time = " + str(self.running_time) + " (ms)\n"
        result += "gc_overhead = " + str(self.gc_overhead) + " (ms)\n"
        result += "avg_cpu_usage = " + str(self.avg_cpu_usage) + "\n"
        result += "max_peak_memory = " + str(self.max_peak_memory) + " (MB)\n"
        return result

def main(string):
    result = Info()

    lst = string.split("/")

    path = ""
    directory = ""
    flag = False
    for i in range(len(lst)-1, -1, -1):
        if flag == False and lst[i] != "":
            directory = lst[i]
            flag = True
        elif flag == True:
            path = lst[i] + "/" + path
    if directory == "":
        print "Invalid directory format."
        return

    lst = directory.split("-")
    if len(lst) < 7:
        print "Invalid directory format."
        return

    result.application_id = "-".join(lst[0:3])
    result.configuration_id = "-".join(lst[3:6])
    result.application_name = lst[6]


    pd = path + directory
    eventlog_fname = ""
    for f in listdir(pd):
        if f.split("-")[0] == "app":
            eventlog_fname = join(pd, f)

    # EventLog
    eventlog = EventLog(eventlog_fname)
    result.running_time = eventlog.app_runtime
    result.gc_overhead = eventlog.gc_time

    # BtraceLogs from all executors
    execdirs = sorted([ d for d in listdir(pd) if isdir(join(pd,d)) ])
    btracelog_fnames = []
    for d in execdirs:
        for f in listdir(join(pd,d)):
            fname = join(pd,d,f)
            if isfile(fname) and fname.split(".")[-1] == "btrace":
                btracelog_fnames.append(fname)

    btracelogs = []
    for fname in btracelog_fnames:
        btracelogs.append(BtraceLog(fname))

    result.max_peak_memory = max([btracelog.max_memory for btracelog in btracelogs])
    cpu = [btracelog.avg_cpu_load for btracelog in btracelogs]
    result.avg_cpu_usage = sum(cpu) / len(cpu)

    print result


import sys
if __name__ == "__main__":
    main(sys.argv[1])
