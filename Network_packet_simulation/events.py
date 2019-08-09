import heapq

class Event:
    def time(self):
        """
        Returns the time at which the event will be processed
        """
        return self.t
    def __str__(self):
        """
        Displays Event
        """
        return self.name + "(" + str( self.t ) + ")"
    def __lt__(self, other):
        """
        Compares the event with another sorted by processing order priority
        """
        return self.t < other.t
    
class EventQueue:
    def __init__(self):
        self.q = []
    def notEmpty(self):
        """
        Returns true if the queue is not empty
        """
        return len(self.q) > 0
    def remaining(self):
        """
        Returns the number of events awaiting processing
        """
        return len(self.q)
    def insert(self, event):
        """ 
        Create a new event in the queue
        """
        heapq.heappush( self.q, event )
    def next(self):
        """
        Returns and removes from the queue the next event to be processed
        """
        return heapq.heappop( self.q )
    
    def reset(self):
        self.q = []