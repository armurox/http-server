from exceptions import MalformedRequestException
from exceptions import HttpNotFoundError

def handle_request(connection):
    try:
        result = connection.recv(1024)
        print(result)
        request = HttpRequest(result)
        print('The parsed request is', request.parsed_request)
        response = HttpResponse(request).response
        print('Response is', response)
        connection.sendall(response)
    except MalformedRequestException:
        connection.sendall('HTTP/1.1 400 Bad Request\r\n\r\n'.encode('utf-8'))
    except HttpNotFoundError:
        connection.sendall('HTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8'))
    connection.close()


class HttpRequest:
    def __init__(self, request):
        try:
            self.original_request = request
            self.decoded_request = self.original_request.decode('utf-8').split('\r\n')
            self.request_method = self.decoded_request[0].split(' ')[0]
            self.path = self.decoded_request[0].split(' ')[1]
            self.http_version= self.decoded_request[0].split(' ')[2]
            self.headers = {}
            rest_of_request = self.decoded_request[1:]
            for i in range(len(rest_of_request)):
                if rest_of_request[i] == '':
                    self.request_body = '\r\n'.join(rest_of_request[i+1:])
                    break
                key, value = rest_of_request[i].split(': ')
                self.headers[key.lower()] = value
        except IndexError:
            raise MalformedRequestException('Malformed Http Request! Please confirm you are following the correct http protocol')
    
    @property
    def parsed_request(self):
        return {
                    'request_method': self.request_method,
                    'path': self.path,
                    'http_version': self.http_version,
                    'headers': self.headers,
                    'request_body': self.request_body,
        }
    

class HttpResponse:
    def __init__(self, request):
        self.request = request
        self.http_version = self.request.http_version
        self._headers = self.request.headers
    
    @property
    def headers(self):
        return HttpResponseHeaders(self._headers)  # Wrapping this in a class to keep track of when it modified accessed
    
    @property
    def allowed_paths(self):
        return {
            '/': lambda _, a :'Hello and welcome!',
            '/user-agent': lambda _, a: self.request.headers['user-agent']
        }
    
    @property
    def response(self):
        if self.request.path in self.allowed_paths:
            self.status_line = 'HTTP/1.1 200 OK'
            self.response_body = self.allowed_paths.get(self.request.path)(self.request, self.headers)
            return '\r\n'.join([self.status_line,
                                '\r\n'.join([f'{header}: {self._headers[header]}' for header in self._headers]) + '\r\n',
                                self.response_body]).encode('utf-8')
        raise HttpNotFoundError('Not a valid path!')


class HttpResponseHeaders:
    def __init__(self, headers):
        self.headers = headers
        self.modified = False
    
    def __setitem__(self, key, val):
        self.modified = True
        self.headers[key] = val
    
    def __getitem__(self, key):
        return self.headers[key]
