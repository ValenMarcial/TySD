from bottle import route, run, static_file, request
from datetime import datetime
from wsgiref.simple_server import WSGIRequestHandler


class ClientAddressHandler(WSGIRequestHandler):
    def get_environ(self):
        environ = super().get_environ()
        environ['REMOTE_PORT'] = str(self.client_address[1])
        return environ


@route('/')
def server_static():
    return static_file('index.html', root='./public')

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./public')

# serve /time resource
@route('/time')
def time():
    t = datetime.now()
    return {"hour": t.hour, "minutes": t.minute, "seconds": t.second}

@route('/client-address')
def client_address():
    return {
        "ip": request.remote_addr,
        "port": int(request.environ['REMOTE_PORT']),
    }

if __name__ == '__main__':
    run(
        host='localhost',
        port=8080,
        debug=True,
        handler_class=ClientAddressHandler,
    )
