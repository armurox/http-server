import socket

def main():
    server = socket.create_server(('localhost', 8080), reuse_port=True)
    connection, address = server.accept()
    print('Accepted connection from client with address', address)
    # Implement 200 or 404 at root address
    request = connection.recv(1024).decode('utf-8').split()
    connection.sendall(b'HTTP/1.1 200 OK\r\n\r\n' if request[1] == '/' else b'HTTP/1.1 404 Not Found\r\n\r\n')
    
    
if __name__ == '__main__':
    main()
