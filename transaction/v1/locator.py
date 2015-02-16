from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
             


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
        
        markable = yield self.call('data.is_markable', pos)
        next_existing = yield self.call('data.is_pos', next_pos)
        
        if markable and next_existing:
            self.call('data.mark_pos', pos)
            self.call('data.set_position', next_pos)
        elif not markable:
            self.publish(
                'error', 
                'The pos {} is not markable.'.format(pos)
            )
        else:
            self.publish(
                'error', 
                'The pos {} does not exist.'.format(next_pos)
            )
        
        # Always done    
        self.call('data.sth')
        
        
if __name__ == "__main__":
    print('Starting Locator component...')
    
    ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1').run(Locator)
