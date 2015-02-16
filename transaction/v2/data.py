from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class PositionError(ValueError):
    pass

class Data(ApplicationSession):

    DIRECTIONS = (-1, 1)

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        
        self.positions = ['', '', '', '', '', '']
        self.markables = [True, True, False, True, False, False]
        self.position = 0
        self.direction = 1

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self)
    
    @wamp.register(u'data.get_direction')    
    def get_direction(self):
        return self.direction
    
    @wamp.register(u'data.get_position')    
    def get_position(self):
        return self.position
    
    @wamp.register(u'data.mark_pos')    
    def mark_pos(self, pos):
        try:
            assert self.markables[pos]
        except IndexError:
            raise PositionError('The position {} does not exist.'.format(pos))
        except AssertionError:
            raise PositionError('The position {} is not markable.'.format(pos))
            
        yield
        
        self.positions[pos] = 'marked'
        
        print('Positions: {}'.format(self.positions))
        
    @wamp.register(u'data.set_position')    
    def set_position(self, pos):
        try:
            self.positions[pos]
        except IndexError:
            raise PositionError('The position {} does not exist.'.format(pos))
    
        yield
        
        self.position = pos
        
        print('Position: {}'.format(self.position))
        
        
if __name__ == "__main__":
    print('Starting Data component...')
    
    ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1').run(Data)
