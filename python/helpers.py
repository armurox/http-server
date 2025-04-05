from constants import ALLOWED_METHODS
from constants import ALLOWED_PATHS

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
        response['status_line'] = 'HTTP/1.1 200 OK'
        response['headers']['Content-Type'] = 'text/plain' if not request['headers'].get('content-type') else request['headers'].get('content-type')
        try:
            response['response_body'] = {'': '',
                                        'echo': request['path'].split('/')[2],
                                        'user-agent': request['headers'].get('user-agent') or '',
                                        'request-body': request['request_body']}.get(path_start)
            response['headers']['Content-Length'] = len(response['response_body'])
        except IndexError:
            response['response_body'] = {'': '',
                                        'user-agent': request['headers'].get('user-agent') or '',
                                        'request-body': request['request_body']}.get(path_start)
            response['headers']['Content-Length'] = len(response['response_body'])
            
    return '\r\n'.join((response['status_line'], 
                        '\r\n'.join([f'{header}: {response['headers'][header]}' for header in response['headers']]) + '\r\n', 
                        response['response_body'])).encode('utf-8')

def handle_request(connection):
    connection.sendall(construct_response(parse_request(connection.recv(1024))))
    connection.close()
