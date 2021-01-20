# Version 1.00
import threading
import socket
#import argparse
import os
import time

bookmarksFile = "bookmarks.txt"

def createFiles():
    f = open(bookmarksFile, "a")

def bookmarkExist(newBookmark):
    with open(bookmarksFile, "r") as bookmark:
        bookmarks = bookmark.read()
        if newBookmark in bookmarks:
            return True
        else:
            return False



def createBookmark(host, port):
    newBookmark = "{}:{}".format(host, port)
    if not bookmarkExist(newBookmark):
        with open(bookmarksFile, "a") as bookmark:
            name = input("Enter name for bookmark:")
            newBookmark = "{}: {}".format(name, newBookmark)
            bookmark.write(newBookmark)
            print("{} added to bookmarks!".format(newBookmark))
    else:
        print("Bookmark already exists!")

def clearWindow():
    os.system('cls' if os.name == 'nt' else 'clear')

def milliTime():
    return round(time.time() * 1000)

# Determines the time elapsed from start to current time
def timeElapsed(start):
    return milliTime() - start

def cmd_quit(args):
    cmd_disconnect(args)
    print("Closing application...")
    os._exit(0)

def cmd_help(args):
    print("help")

def cmd_bookmark(args):
    createBookmark(client.host, client.port)

def cmd_disconnect(args):
    client.sock.close()
    clearWindow()
    print('\nDisconnected.')



commandPrefix = "/"
helpCommand = "help"
quitCommand = "quit"

commandList = {
    quitCommand: cmd_quit,
    helpCommand: cmd_help,
    "bookmark": cmd_bookmark
    #"disconnect": cmd_disconnect Currently erroring

}

def invalidCommand():
    print("Unknown command, type {}{} for information.".format(commandPrefix, helpCommand))

def executeCommand(command, args):
    if command in commandList:
        commandList[command](args)
    else:
        invalidCommand()



class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            message = input('{}: '.format(self.name))

            if message == "":
                continue

            if message[0] == commandPrefix:
                message = message.strip(commandPrefix).split(" ")
                command = message[0]
                message.remove(command)
                args = message
                executeCommand(command, args)
            else:
                # Send message to server for broadcasting
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

            # Type 'QUIT' to leave the chatroom
            if message == quitCommand:
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break



class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            message = self.sock.recv(1024)
            if message:
                print('\r{}\n{}: '.format(message.decode('ascii'), self.name), end = '')
            else:
                # Server has closed the socket, exit the program
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        name = input('Your name: ')
        clearWindow()
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        startTime = milliTime()
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}. Took {}ms'.format(self.host, self.port, timeElapsed(startTime)))

        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(name))

        # Create send and receive threads
        send = Send(self.sock, name)
        receive = Receive(self.sock, name)

        # Start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. Say hi!'.format(name).encode('ascii'))
        print("\rAll set! Leave the chatroom anytime by typing {}{}\n".format(commandPrefix, quitCommand))
        print('{}: '.format(name), end = '')

if __name__ == '__main__':
    createFiles()
    clearWindow()
    #parser = argparse.ArgumentParser(description='Chatroom Server')
    #parser.add_argument('host', help='Interface the server listens at')
   # parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                              #  help='TCP port (default 1060)')
    #args = parser.parse_args()

    host = input('Enter IP to connect to: ')
    client = Client(host, 1060)
    client.start()



