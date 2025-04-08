import gzip
ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'PATCH']
ALLOWED_PATHS = ['', 'echo', 'user-agent', 'request-body', 'files']
ALLOWED_ENCODINGS = {'gzip': gzip.compress}
