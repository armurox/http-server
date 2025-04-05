import socket
from helpers import parse_request
from helpers import construct_response

def main():
    server = socket.create_server(('localhost', 8080), reuse_port=True)
    connection, address = server.accept()
    print('Received connection from address %s', address)
    request = parse_request(connection.recv(1024))
    connection.sendall(construct_response(request))
    
    
if __name__ == '__main__':
    main()
