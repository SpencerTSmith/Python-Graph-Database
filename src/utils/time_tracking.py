import time
from typing import Optional
class LamportClock:
    def __init__(self):
        self.clock=0
    def increment(self):
        self.clock+=1
        return self.clock
    def receive_event(self,received_clock):
        self.clock=max(self.clock,received_clock)+1
        return self.clock
    
class TimeTracking:
    def __init__(self, log_file: Optional[str]='event.log'):
        self.lamport_clock=LamportClock()
        self._log_file=log_file
        open(self._log_file,'w')

    def get_lamport_times(self):
        lamport_time=self.lamport_clock.increment()
        return lamport_time
    
    def _log_times(self, action: str, start_time: float, end_time: float, lamport_time: int):
        with open(self._log_file, 'a') as f:
            f.write(f"Action: {action}\n")
            f.write(f"Start Time (Unix): {start_time}\n")
            f.write(f"End Time (Unix): {end_time}\n")
            f.write(f"Duration: {end_time - start_time:.6f} seconds\n")
            f.write(f"Lamport Clock Time: {lamport_time}\n")
            f.write("-" * 40 + "\n")
