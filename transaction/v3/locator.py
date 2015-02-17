from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
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
        
        try:
            yield self.call('data.check_markable', pos)
            yield self.call('data.check_position', next_pos)
        except ApplicationError as e:
            raise e
        else:
            self.call('data.mark_position', pos)
            self.call('data.set_position', next_pos)
        finally:
            try:
                yield self.call('data.check_sth')
            except ApplicationError as e:
                raise e
            else:
                self.call('data.do_sth')
        
        
if __name__ == "__main__":
    print('Starting Locator component...')
    
    ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1').run(Locator)
