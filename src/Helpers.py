import threading
import Queue

# stopper class
class StopMe:
    stopper = None
    workers = None

    def __init__(self, stopper, workers):
        self.stopper = stopper
        self.workers = workers

    # When called will kill all running threads
    def stop(self):
        self.stopper.set()
        for worker in self.workers:
            worker.join()
        
        print("PROGRAM STOPPED!")

# Sequence Analysis Data Object
# Holds all items needed for analysis
class SeqData:
    p_ID = None
    path = None
    seq_config = None

    def __init__(self, p_ID, path, seq_config):
        self.p_ID = p_ID
        self.path = path
        self.seq_config = seq_config