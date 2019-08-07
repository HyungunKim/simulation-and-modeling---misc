from collections import namedtuple

Request = namedtuple("Request", ["arrived_at", "time_to_process"])
Response = namedtuple("Response", ["was_dropped", "started_at"])

class Buffer:
    def __init__(self, size):
        self.size = size
        # self.finish_time is a queue for
        # keeping track of finishing time of packets to compare with new packet's arrical time.
        self.finish_time = [] 
                              
    def process(self, request): # process methods returns approprient Resopnse.
        time = -1
        dropped = True
        free = False
        for i in range(self.size):
            if len(self.finish_time) == 0: # handling the case where Buffer is intirely free.
                free = True   
                dropped = False
                break
            if request.arrived_at >= self.finish_time[0]: # In this case Buffer gets free space thus current request doesn't drop.
                # skipping time to current request's arrival time.
                # in doing so finished requests are popped from the queue.
                self.finish_time.pop(0) # As a queue, first in is first out (fifo).
                dropped = False 
            else: # Need to chech if Buffer has free space. see below (line 40)
                break
        if len(self.finish_time) == 0: # Double checks if Buffer is free.
            free = True   
            dropped = False
            
        if not dropped: # this case we are sure it's not dropped.
            if free: # Buffer is free, current request is processed at it's arrival time.
                time = request.arrived_at
            else:
                time = self.finish_time[-1] # current request is processed when the last element in queue is done.
            self.finish_time.append(time + request.time_to_process) # Append to queue when current request is done.
        
        elif len(self.finish_time) < self.size: # Checking if Buffer has free space
            dropped = False
            time = self.finish_time[-1]
            self.finish_time.append(time + request.time_to_process)
        
        return Response(dropped, time)



def process_requests(requests, buffer):
    responses = []
    for request in requests:
        responses.append(buffer.process(request))
    return responses


    