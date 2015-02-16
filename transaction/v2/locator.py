from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

from tools import Transaction
             


class Locator(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self)
        
    @wamp.register(u'locator.move')
    @inlineCallbacks
    def move(self):
        """Try to mark the current position and to go to the next one. Fail if 
        the current position is not markable or if the next position does not 
        exist.
        """
        
        print('Move!')
        
        pos = yield self.call('data.get_position')
        direction = yield self.call('data.get_direction')
        next_pos = pos + direction
        
        mark_pos_gen = yield self.call('data.mark_pos', pos)
        set_pos_gen = yield self.call('data.set_position', next_pos)
        
        self.call('data.sth') # Always done
        
        Transaction([mark_pos_gen, set_pos_gen]).start()
        
        
if __name__ == "__main__":
    print('Starting Locator component...')
    
    ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1').run(Locator)
