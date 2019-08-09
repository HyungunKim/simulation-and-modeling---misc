import numpy as np
from events import Event, EventQueue


class Buffer:
    def __init__(self, size):
        self.size = size # constant size of buffer
        self.Q = 0 # queue of packets. 
        self.t = 0 # time tracker
        self.dropped = 0 # number of dropped packets.
    def is_empty(self):
        if self.Q == 0:
            return True
        else:
            return False
    
    def available(self):
        if self.Q < self.size:
            return True
        else:
            return False
        
    def time(self, dT=0):
        self.t += dT
        return self.t
    def set_time(self, T):
        self.t = T
    
    def enQ(self):
        self.Q += 1
        
    def deQ(self):
        self.Q -= 1
    
    def drop(self):
        self.dropped += 1
        
    def num_dropped(self):
        return self.dropped

    def reset(self):
        self.Q = 0
        self.dropped = 0

class arrival(Event):
    def __init__(self, arrival_time, process_time):
        self.t = arrival_time
        self.process_time = process_time
    def action(self, queue, buffer):
        if buffer.is_empty():
            buffer.enQ()
            buffer.set_time(self.t + self.process_time)
            queue.insert(returned((buffer.time())))
        elif buffer.available():
            buffer.enQ()
            queue.insert(returned(buffer.time(dT = self.process_time)))
        else:
            buffer.drop()

class returned(Event):
    def __init__(self, processed_time):
        self.t = processed_time
    def action(self, queue, buffer):
        buffer.deQ()
        

def tester(buffer_size, rps, num_packets = 100, num_tests = 1000):
    
    # we are testing in milliseconds
    # or milli unit time, as it can be scaled naturally.
    lam = rps/1000
    
    # beta is average time interval between two arrival events. (measured compared to processing speed)
    beta = 1/lam
    
    # just using Rayleigh distribution for processing time of requests. 
    # Can play around with other distributions such as Maxwell-Boltzmann.
    arrival_times = np.random.exponential(beta, (num_tests, num_packets))
    process_times = np.random.rayleigh(1, (num_tests, num_packets)) 
    
    buffer = Buffer(buffer_size)
    dropped = np.zeros(num_tests)
    
    for i in range(num_tests):
        arrival_time = 0
        Q = EventQueue()
        for j in range(num_packets):
            arrival_time += arrival_times[i,j]
            process_time = process_times[i,j]
            Q.insert(arrival(arrival_time, process_time))
        
        while Q.notEmpty():
            e = Q.next()
            e.action(Q, buffer)
        
        dropped[i] = buffer.num_dropped()
        buffer.reset() # restarting buffer for next test.
        Q.reset() # restarting queue for next test.
    return dropped

    
