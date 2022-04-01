from operating_sys import Job, OperatingSystem
from random import shuffle

class Scheduler:
    def __init__(self, jobs):
        self.jobs = jobs
        self.current_job = None
        self.time = 0

    def update(self, time):
        "Returns: 0 holds, 1: change, 2: finish"
        for job in self.jobs:
            job.update(time)
        self.time = time

        prev_job = self.current_job
        self.current_job = self.get_next_job()      
        
        if self.current_job.state == 3 and not self.are_jobs_incoming():
            return 2
        
        if self.current_job.state <= 1:
            self.current_job.set_state(1, time)
                
        return 0 if prev_job == self.current_job else 1

    def get_current_jobs(self):
        jobs = [job for job in self.jobs if job.state < 2]
        shuffle(jobs)
        return jobs

    def are_jobs_incoming(self):
        return len([job for job in self.jobs if job.state == 4]) > 0


class FIFO(Scheduler):
    def get_next_job(self):
        current_jobs = self.get_current_jobs()
        if self.current_job is None or self.current_job.state == 3 or  self.current_job.state == 2:
            return min(current_jobs, default=self.current_job, key=lambda x: x.arrival_time)
        return self.current_job


class SJF(Scheduler):
    def get_next_job(self):
        current_jobs = self.get_current_jobs()
        if self.current_job is None or self.current_job.state == 3 or self.current_job.state == 2:
            return min(current_jobs, default=self.current_job, key=lambda x: x.completion_time)
        return self.current_job


class STCF(Scheduler):
    def get_next_job(self):
        current_jobs = self.get_current_jobs()
        if self.current_job is not None and self.current_job.state == 1:
            self.current_job.set_state(0, self.time)
        return min(current_jobs, default=self.current_job, key=lambda x: x.completion_time-x.run_time)


class RoundRobin(Scheduler):
    def __init__(self,jobs, ei):
        Scheduler.__init__(self,jobs)
        self.ei = ei
        self.job_start_time = 0
        self.cycle = []


    def get_next_job(self):
        # Fill cycle
        if not self.cycle:
            self.cycle = self.get_current_jobs()
            self.job_start_time = self.time
            if not self.cycle:
               return self.current_job
        current_job = self.cycle[0]
        
        # Cycle time is done or jobs is blocked
        if self.time - self.job_start_time >= self.ei or current_job.state == 2 or current_job.state == 3: 
            self.cycle.pop(0)
            if current_job.state == 1:
                current_job.set_state(0, self.time)
            if not self.cycle: 
                return self.get_next_job() # The cycle is empty and reRun method to Fill it 
            self.job_start_time = self.time
        
        return self.cycle[0]