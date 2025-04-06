# Background

Welcome to this repo! This is a record me creating an http-server in multiple languages (currently python) in order to understand how they work more deeply. Have fun!

Features:
- Complete parsing of and http request into `headers`, `path`, `method` and `body`
- Parses request in and returns response in [origin-form](https://datatracker.ietf.org/doc/html/rfc9112#section-3.2.1)
- Allows serving and creation of files, including html files.

Current Paths of the http server:

1. `GET /` - Root, simply returns `HTTP/1.1 200 OK\r\n`
2. `GET /echo/QUERY` -  Simply echos back `QUERY` in the response body.
3. `GET /user-agent` - Returns the user-agent provided in the request back in the response body.
4. `GET files/FILEPATH` - Returns the file details of the specified file or `HTTP/1.1 404 Not Found\r\n`
5. `POST files/FILEPATH` - Creates the file in the static directory.
