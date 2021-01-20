import threading
import socket
import argparse
import os
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
time_stamp_formatting = '{}: '.format(current_time)

class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))

        sock.listen(1)
        print('{}Listening at'.format(time_stamp_formatting), sock.getsockname())

        while True:
            # Accept new connection
            sc, sockname = sock.accept()
            print('{}Accepted a new connection from {} to {}'.format(time_stamp_formatting, sc.getpeername(), sc.getsockname()))

            # Create new thread
            server_socket = ServerSocket(sc, sockname, self)

            # Start new thread
            server_socket.start()

            # Add thread to active connections
            self.connections.append(server_socket)
            print('{}Ready to receive messages from'.format(time_stamp_formatting), sc.getpeername())

    def broadcast(self, message, source):

        for connection in self.connections:

            # Send to all connected clients
                connection.send('{}{}'.format(time_stamp_formatting,message))


class ServerSocket(threading.Thread):

    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):

        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                print('{}{} says {!r}'.format(time_stamp_formatting, self.sockname, message))
                self.server.broadcast(message, self.sockname)
            else:
                # Client has closed the socket, exit the thread
                print('{}{} has closed the connection'.format(time_stamp_formatting, self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode('ascii'))

    def exit(server):

        while True:
            ipt = input('')
            if ipt == 'q':
                print('{}Closing all connections...'.format(time_stamp_formatting))
                for connection in server.connections:
                    connection.sc.close()
                print('{}Shutting down the server...'.format(time_stamp_formatting))
                os._exit(0)

    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Chatroom Server')
        parser.add_argument('host', help='Interface the server listens at')
        parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                            help='TCP port (default 1060)')
        args = parser.parse_args()

        # Create and start server thread
        server = Server(args.host, args.p)
        server.start()

        exit = threading.Thread(target=exit, args=(server,))
        exit.start()
