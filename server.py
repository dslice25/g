import json
from twisted.internet import reactor, protocol, task


class GameProtocol(protocol.Protocol):
  
  def __init__(self, factory, addr):
    self.factory       = factory
    self.addr          = addr
    self.player_id     = None
    self.authenticated = False
    
  def connectionMade(self):
    print "Connection from {}:{}".format(self.addr.host,self.addr.port)

  def connectionLost(self, reason):
    print "Disconnection from {}:{} ({})".format(self.addr.host,self.addr.port,reason.getErrorMessage())

  def dataReceived(self, data):
    
    try:
      request_data = json.loads(data)
    except:
      print "Could not process data {}".format(data)
      return

    try:
      request_type = request_data['type']
    except:
      print "No type specified in request_data ({})".format(request_data)
      return

    if request_type == 'login':
      if self.authenticated:
        return

      try:
        self.factory.login(request_data['username'],request_data['password'])
      except:
        print "Could not login ({})".format(request_data)
      
      return
      
    if not self.authenticated:
      return

    if request_type == 'getmap':
      pass
    
    elif request_type == 'getinv':
      pass

    elif request_type == 'pickup':
      pass
        
    elif request_type == 'move':
      pass
    
    elif request_type == 'drop':
      pass

    elif request_type == 'logout':
      pass

  def relayEvents(self):
    for event in self.factory.events[self.last_event:]:
      if event['id'] != self.conn_id:
        self.transport.write(event['data'])

    self.last_event = len(self.factory.events)

class GameServerFactory(protocol.ServerFactory):

  def __init__(self):
    
    self.events = []
    self.users  = {}

  def login(self, username, password):
    return True

  def buildProtocol(self, addr):
    return GameProtocol(self, addr) 

def main():
  reactor.listenTCP(8000,GameServerFactory())
  reactor.run()

if __name__ == '__main__':
  main()
