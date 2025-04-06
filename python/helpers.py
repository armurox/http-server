from constants import ALLOWED_METHODS
from constants import ALLOWED_PATHS
import os
from exceptions import HttpNotFoundError

def parse_request(request):
    parsed_request = {'method': '', 'path': '', 'headers': {}, 'http_version': '', 'request_body': ''}
    split_request = request.decode('utf-8').split('\r\n')
    request_line = split_request[0].split()
    parsed_request.update(
        {
            'method': request_line[0], 
            'path': request_line[1],
            'http_version': request_line[2].split('/')[1]
        }
    )
    
    rest_of_request = split_request[1:]
    for i in range(len(rest_of_request)):
        if rest_of_request[i] == '':
            parsed_request['request_body'] = '\r\n'.join(rest_of_request[i + 1:])
            break
        header = rest_of_request[i].split(': ')
        parsed_request['headers'][header[0].lower()] = header[1]
    print('The parsed request is', parsed_request)
    return parsed_request


def construct_response(request):
    response = {'status_line': '', 'headers': {}, 'response_body': ''}
    path_start = request['path'].split('/')[1]
    if request['method'] not in ALLOWED_METHODS:
        response['status_line'] = 'HTTP/1.1 405 Method Not Allowed'
        return response['status_line']
    elif path_start not in ALLOWED_PATHS:
        response['status_line'] = 'HTTP/1.1 404 Not Found'
    else:
        try:
            response['status_line'] = 'HTTP/1.1 200 OK'
            response['headers']['Content-Type'] = 'text/plain' if not request['headers'].get('content-type') else request['headers'].get('content-type')
            response['response_body'] = {'': lambda request, response : '',
                                        'echo': lambda request, response: request['path'].split('/')[2],
                                        'user-agent': lambda request, response: request['headers'].get('user-agent') or '',
                                        'request-body': lambda request, response: request['request_body'],
                                        'files': return_or_create_file}.get(path_start)(request, response)
            response['headers']['Content-Length'] = len(response['response_body'])
        except HttpNotFoundError:
            response = {'status_line': 'HTTP/1.1 404 Not Found', 'headers': {}, 'response_body': ''}
            
    return '\r\n'.join((response['status_line'], 
                        '\r\n'.join([f'{header}: {response['headers'][header]}' for header in response['headers']]) + '\r\n', 
                        response['response_body'])).encode('utf-8')



def handle_request(connection):
    connection.sendall(construct_response(parse_request(connection.recv(1024))))
    connection.close()


def return_or_create_file(request, response):
    if request['method'] == 'GET':
        try:
            with open(os.path.join('/tmp', request['path'].split('/')[2]), 'r') as f:
                response_body = f.read()
                response['headers']['Content-Type'] = 'application/octet-stream'
                return response_body
        except FileNotFoundError:
            raise HttpNotFoundError
    elif request['method'] == 'POST':
        with open(os.path.join('/tmp', request['path'].split('/')[2]), 'w') as f:
                f.write(request['request_body'])
                response['status_line'] = 'HTTP/1.1 201 Created'
                return ''
