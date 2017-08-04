import tornado.ioloop
import tornado.web

from app.listener import Listener


def make_app():
    return tornado.web.Application([
        (r"/", Listener),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8112)
    tornado.ioloop.IOLoop.current().start()