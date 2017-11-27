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
    its_dict = None
    seq_config = None

    def __init__(self, its_dict, seq_config):
        self.its_dict = its_dict
        self.seq_config = seq_config