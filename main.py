from pprint import pprint
import numpy as np
from scheluder import *
from operating_sys import OperatingSystem, Job
from copy import deepcopy

def get_input():
    n = int(get_line())
    a = get_int_lines()
    if len(a) == 1:
        q = a[0]
        c = 0
    elif len(a) == 2:
        q, c = a
    time_slices = get_int_lines()
    lines = []
    while n > 0:
        a = get_data()
        lines.append(a)
        n -= 1
    return lines, q, time_slices, c

def get_data():
    line = input().split()
    result = [int(line[0]), int(line[1])]
    for io in line[2:]:
        temp = io.split('-')
        result += [int(temp[0]), int(temp[1])]
    return result


def get_int_lines():
    try:
        return [int(ei) for ei in get_line().split()]
    except ValueError:
        raise ValueError(int)

def get_line():
    line = input()
    while not line or line[0] == '#':
        line = input()
    try:
        idx = line.index('#')
        line = line[:idx]
    except ValueError:
        pass
    return line

def build_jobs(lines):
    jobs = []
    for line in lines:
        interruptions = [(line[i], line[i+1]) for i in range(2, len(line), 2)]
        jobs.append(Job(line[0], line[1], interruptions))
    return jobs


def turn_around_time(job):
    return job.finish_time - job.arrival_time


def response_time(job):
    return job.first_run_time - job.arrival_time


def print_output(outs, avg):
    for out in outs:
        print(' '.join(str(i) for i in out))
    print()
    for method in avg:
        print(' '.join(str(j) for j in method))



def calculate_avg(outs, all_jobs):
    avarages = []
    for i in range(0, len(outs[0]), 2):
        avarages.append([round(np.average(outs[:, i]), 3),  round(np.average(outs[:, i+1]), 3)]) 
    for i, jobs in enumerate(all_jobs):
          avarages[i].append(max(job.finish_time for job in jobs)) 
    return avarages
    

def build_all_outputs(all_jobs):
    "Recieve all jobs returned by all the algorithms"
    outs = build_output([[] for _ in all_jobs[0]], all_jobs[0])
    for jobs in all_jobs[1:]:
        outs = build_output(outs, jobs)
    return np.array(outs)


def build_output(original, jobs):
    result = list(original)
    for i in range(len(original)):
        result[i] += [turn_around_time(jobs[i]), response_time(jobs[i])]
    return result


def pprint_jobs(all_jobs):
    print('-----------------FIFO-----------------')
    pprint(all_jobs[0])
    print('------------------SJF------------------')
    pprint(all_jobs[1])    
    print('-----------------STCF------------------')
    pprint(all_jobs[2])
    for i in range(len(all_jobs[3:])):
        print('------------------RR_%s-------------------' % i)
        pprint(all_jobs[i])
    print()    


if __name__ == '__main__':
    # lines, quantum_time, ei, cxt_time = get_input()
    lines = [[0, 10, 5, 5, 6, 5], [5, 6, 2, 6]]
    lines = [[0, 100], [10, 10], [10, 10]]
    ei = [10, 15, 5]
    quantum_time = 5
    cxt_time = 0
    jobs = build_jobs(lines)
    

    # scheduler = scheduler(deepcopy(jobs))
    os = OperatingSystem(quantum_time, cxt_time)
    out_fifo = os.execute(jobs, FIFO(deepcopy(jobs)))
    out_sjf = os.execute(jobs, SJF(deepcopy(jobs)))
    out_stcf = os.execute(jobs, STCF(deepcopy(jobs)))
    outs_rr = []
    for e in ei:
        outs_rr.append(os.execute(jobs, RoundRobin(deepcopy(jobs), e)))
   
    all_jobs = [out_fifo, out_sjf, out_stcf, *outs_rr]
    # pprint_jobs(all_jobs)
    outs = build_all_outputs(all_jobs)
    print_output(outs, calculate_avg(outs, all_jobs))
