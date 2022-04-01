class OperatingSystem:
    def __init__(self, quantum_time, context_time):
        self.quantum_time = quantum_time
        self.context_time = context_time
    
    def execute(self, jobs, scheduler):
        current_time = 0
        while True:
            response = scheduler.update(current_time)
            current_time += self.quantum_time
            if response == 2:
                break
            elif response == 1:
                current_time += self.context_time
        return scheduler.jobs


class Job:
    # self.state = 0: ready, 1: running, 2: blocked, 3: completed, 4: unarrived
    def __init__(self, arrival_time, completion_time, interruptions):
        self.arrival_time = arrival_time
        self.completion_time = completion_time
        self.interruptions = interruptions
        self.state = 4
        self.run_time = 0
        self.first_run_time = -1

    def set_state(self, state, time):
        self.state = state
        if state == 1:
            if self.first_run_time == -1:
                self.first_run_time = time
            self.start_run_time = time
        if state == 2:
            self.start_block_time = time
        if state == 3:
            self.finish_time = time


    def update(self, time):
        if self.state == 4 and self.arrival_time <= time:
            self.state = 0
        
        elif self.state == 1:
            delta_time = time - self.start_run_time
            inter = self._get_interruption(self.run_time + 1, delta_time + self.run_time)
            if inter is None:
                if self.run_time + delta_time >= self.completion_time:
                    self.set_state(3, self.start_run_time + self.completion_time - self.run_time)
                self.run_time += delta_time
            else:
                self.set_state(2, self.start_run_time + inter[0] - self.run_time)
                self.run_time = inter[0]
        
        if self.state == 2:
            delta_time = time - self.start_run_time
            inter = self._get_interruption(self.run_time, delta_time + self.run_time)
            if time - self.start_block_time >= inter[1]:
                self.set_state(0, time)
        
    def __repr__(self):
        return f'runtime: {self.run_time}, start: {self.first_run_time}, finish time {self.finish_time}'

    def _get_interruption(self, start, end):
        for i in self.interruptions:
            if start <= i[0] <= end:
                return i
        return None 