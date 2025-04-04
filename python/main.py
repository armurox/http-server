import socket

def main():
    server = socket.create_server(('localhost', 8080), reuse_port=True)
    connection, address = server.accept()
    print('Accepted connection from client with address', address)
    # Implement 200 or 404 at root address
    request = connection.recv(1024).decode('utf-8').split()
    request_path = request[1].split('/')
    if 'User-Agent:' in request:
        user_agent_index = request.index('User-Agent:') + 1
    else:
        user_agent_index = 0
    try:
        VALID_PATHS = {'': b'HTTP/1.1 200 OK\r\n\r\n', 
                    'echo': 'HTTP/1.1 200 OK\r\n'
                    'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(request_path[2])}\r\n'
                    f'\r\n{request_path[2]}'.encode('utf-8'),
                    'user-agent': 'HTTP/1.1 200 OK\r\n'
                    'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(request[user_agent_index])}\r\n'
                    f'\r\n{request[user_agent_index]}'.encode('utf-8')}
    except IndexError:
        VALID_PATHS = {'': b'HTTP/1.1 200 OK\r\n\r\n', 'user-agent': 'HTTP/1.1 200 OK\r\n'
                    'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(request[user_agent_index])}\r\n'
                    f'\r\n{request[user_agent_index]}'.encode('utf-8')}
    if response := VALID_PATHS.get(request_path[1]):
        pass
    else:
        response = b'HTTP/1.1 404 Not Found\r\n\r\n'
    connection.sendall(response)
    
    
if __name__ == '__main__':
    main()
