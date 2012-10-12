import tornado.autoreload
import tornado.httpserver
import tornado.websocket
import tornado.options
import tornado.ioloop
import tornado.escape
import tornado.web
import os.path
import os


# User function for writing to WebSocket
def SendRPC(_method, _params, _id):
    print('sending SendRPC')
    if _id == 'everyone':
        for idx, val in enumerate(ClientList.clients):
            # print(idx)
            message = dict(method=_method, params=_params, id=idx)
            ClientList.clients[idx].write_message(message)
    else:
        message = dict(method=_method, params=_params, id='0')
        ClientList.clients[_id].write_message(message)


# Private function to message all clients
def SendEveryoneRPC(_method, _params):
    message = dict(method=_method, params=_params)
    for idx, val in enumerate(ClientList.clients):
        ClientList.clients[idx].write_message(message)


class Doople(object):
    doople = ''


# Stores list of connected clients
class ClientList(object):
    clients = []


# Renders template based on site requested
class SitesHandler(tornado.web.RequestHandler):
    def get(self, path):
        # print(path)
        sitehtml = 'sites_html/' + path + '.html'
        if not os.path.exists(sitehtml):
            raise tornado.web.HTTPError(404)

        # Dynamic modules loading
        Doople.doople = __import__("import_py." + path, fromlist=["*"])

        # Instead of importing, you can just exec a module's code
        # execfile("import_py/chat.py")

        self.render(sitehtml, title=path)


# Dynamically renders JS library files by project name
class JSImportHandler(tornado.web.RequestHandler):
    def get(self, path):
        print('requested file: ' + path)
        self.set_header("Content-Type", "text/javascript; charset=UTF-8")
        jsfile = 'import_js/' + path
        if not os.path.exists(jsfile):
            raise tornado.web.HTTPError(404)
        self.render(jsfile)


# WebSocket class
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        ClientList.clients.append(self)
        print('new connection')

    def on_message(self, message):
        json = tornado.escape.json_decode(message)
        print('method received %s, params %s' % (json["method"], json["params"]))
        getattr(Doople.doople, json["method"])(json["params"], SendRPC)

    def on_close(self):
        ClientList.clients.remove(self)
        print('connection closed')


# Web socket application
WSApplication = tornado.web.Application([
    (r'/ws', WSHandler),
# ])
], debug=True)

# File server application
FileApplication = tornado.web.Application([
    (r'/([A-Za-z0-9]+)', SitesHandler),
    (r'/import_js/(.*)', JSImportHandler),
# ])
], debug=True)

if __name__ == "__main__":
    http_server_index = tornado.httpserver.HTTPServer(FileApplication)

    # Single thread
    # http_server_index.listen(80)

    # Forks multiple sub-processes
    http_server_index.bind(80)

    # http_server_index.start()
    http_server_index.start(0)

    http_server = tornado.httpserver.HTTPServer(WSApplication)

    # Single thread
    # http_server.listen(8899)

    # Forks multiple sub-processes
    http_server.bind(8899)
    http_server.start()

    tornado.ioloop.IOLoop.instance().start()
