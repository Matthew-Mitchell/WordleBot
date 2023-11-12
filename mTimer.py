import sys
import time

class mtimer:
    """Example:
    iterable = range(20)

    timer = mtimer(iterable)
    for i in iterable:
        timer.progress(i)
        time.sleep(0.5)
    timer.complete() #optional final summary.
    """
    def __init__(self,iterable, timer_cadence=1):
        self.len_tot = len(iterable)
        self.launch_start = time.time()
        #self.cycle_start = time.time()
        #self.cycle_times = []
        self.timer_cadence = timer_cadence #Number of cycles to check time
        self.estimated_process_length = None
    def printout(self, i):
        timestamp = time.time()
        #cycle_time = timestamp - self.cycle_start
        #self.cycle_times.append(cycle_time)
        #avg_time = mean(self.cycle_times)
        pcomplete = i / self.len_tot
        estimated_process_length = (timestamp - self.launch_start) / pcomplete
        if i == 1:
            #cache initial time estimate
            self.estimated_process_length = estimated_process_length
        if i == self.len_tot:
            tot_time = round(timestamp - self.launch_start,1)
            time_left = f"Complete. Process took: {tot_time}"
        else:
            time_left = round((1-pcomplete)*estimated_process_length, 1)
            time_left = f"Time Remaining: {time_left}"
        bars = "="*int(pcomplete*20)
        spaces = " "*int((1-pcomplete)*20)
        prgrss_bar = f"{i} of {self.len_tot}   [{bars}{spaces}]"
        msg = f"{prgrss_bar} {time_left}"
        sys.stdout.write(f"\r{msg}")
        
    def progress(self, i):
        if (i % self.timer_cadence == 0) and (i!=0):
            self.printout(i)
    def complete(self):
        self.printout(self.len_tot)