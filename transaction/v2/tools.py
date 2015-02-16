import pickle

from autobahn import wamp



def register_generator(*args, **kwargs):
    def decorator(func):
        def reg(*args, **kwargs):
            gen = func(*args, **kwargs)
            
            return pickle.dumps(gen)
    
        return wamp.register(*args, **kwargs)(reg)
        
    return decorator
    

class Transaction:
    
    def __init__(self, generators, unserialize=True):
        if unserialize:
            self.generators = [pickle.loads(gen) for gen in generators]
        else:
            self.generators = generators
            
        self.stop = False
        
    def next(self):
        if self.stop:
            raise StopIteration
        
        for gen in self.generators:
            try: next(gen)
            except StopIteration: self.stop = True

    def start(self):
        while not self.stop:
            self.next()
