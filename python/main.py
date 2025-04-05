import socket
import threading
from helpers import handle_request

def main():
    server = socket.create_server(('localhost', 8080), reuse_port=True)
    while True:
        connection, address = server.accept()
        print('Received connection from address %s', address)
        threading.Thread(target=handle_request, args=(connection,)).start()
    
    
if __name__ == '__main__':
    main()
