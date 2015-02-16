class Transaction:
    
    def __init__(self, generators):
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
