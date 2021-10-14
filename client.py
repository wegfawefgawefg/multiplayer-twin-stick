import pickle

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet import task

from game import Game


class GameClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        return GameClient(Game())

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)


class GameClient(Protocol):
    def __init__(self, game, addr=None):
        self.addr = addr
        self.game = game
        self.game.set_client(self)

    def connectionMade(self):
        print('Client connected.')
        self.game_loop = task.LoopingCall(self.game.run)
        deferred = self.game_loop.start(1/60)
        deferred.addErrback(lambda _: reactor.stop())

    def connectionLost(self, reason):
        print(f'Client disconnected. reason={reason}')

    def dataReceived(self, data):
        state = pickle.loads(data)
        self.game.process_state(state)

    def sendMessage(self, msg):
        print(f'Client send message. message={msg.__dict__}')
        self.transport.write(pickle.dumps({
            'type': msg.type,
            'data': msg.__dict__
        }))


def main():
    reactor.connectTCP('localhost', 8888, GameClientFactory())
    reactor.run()


if __name__ == '__main__':
    main()
