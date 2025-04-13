import socket
from helpers import handle_request

def main():
    server = socket.create_server(('localhost', 8000), reuse_port=True)
    print(server)
    while True:
        conn, addr = server.accept()
        handle_request(conn)
        
    
    
if __name__ == "__main__":
    main()
