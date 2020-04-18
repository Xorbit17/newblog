import tornado.web as web
import tornado.ioloop as ioloop
import os
import database  # Hier wordt code uitgevoerd!!


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_FILE_DIR = os.path.join(CURRENT_PATH, "static")


class MainHandler(web.RequestHandler):
    def get(self, user_id):
        user = database.get_user_by_id(user_id)

        self.write("Het werkt: {}".format(user))


def make_tornado_app():
    return web.Application([
        (r"/static/(.*)", web.StaticFileHandler, {"path": STATIC_FILE_DIR}),
        (r"/(.*)", MainHandler)
    ])


if __name__ == "__main__":
    # Gaat alleen uitgevoerd worden als server.py wordt expliciet gerund en niet
    # bij import
    app = make_tornado_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
