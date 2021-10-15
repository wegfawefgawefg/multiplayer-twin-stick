import bz2
import pickle
from uuid import uuid4

from mpts.game import Game
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol


class Server(Factory):
    def __init__(self):
        self.game = Game(server_mode=True)

        self.game_loop = task.LoopingCall(self.game.update)
        self.game_loop.start(1/60)

        self.clients = {}

        print('waiting for connections')

    def buildProtocol(self, addr):
        client = ServerGameClient(self)
        self.clients[client.id] = client
        return client


class ServerGameClient(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.id = str(uuid4())
        self.factory.game.set_client(self)

    def connectionMade(self):
        print('client connected. id:', self.id)
        self.factory.game.new_player(self.id)

    def connectionLost(self, reason):
        print('Lost connection.  Reason:', reason)
        self.factory.game.remove_player(self.id)

    def connectionFailed(self, reason):
        print('Connection failed. Reason:', reason)

    def updateConnectedClients(self, state):
        for client in self.factory.clients.values():
            client.transport.write(
                bz2.compress(
                    pickle.dumps(state)
                )
            )

    def dataReceived(self, data):
        action = pickle.loads(bz2.decompress(data))
        self.factory.game.process_action(self.id, action)


def main():
    endpoint = TCP4ServerEndpoint(reactor, 8888)
    endpoint.listen(Server())
    reactor.run()
    print('server stopped')


if __name__ == '__main__':
    main()
