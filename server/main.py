import os
import tornado.ioloop
import tornado.web
import tornado.websocket

root = os.path.dirname(__file__)
port = 8080


class SocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        self.connections.add(self)

    def on_message(self, message):
        [client.write_message(message) for client in self.connections]

    def on_close(self):
        self.connections.remove(self)


app = tornado.web.Application(
    [
        (r"/websocket", SocketHandler),
        (
            r"/(.*)",
            tornado.web.StaticFileHandler,
            {"path": root, "default_filename": "index.html"},
        ),
    ]
)

if __name__ == "__main__":
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()
