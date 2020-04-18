import tornado.web as web
import tornado.ioloop as ioloop
import os
import hashlib
import database  # Hier wordt code uitgevoerd!!

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_FILE_DIR = os.path.join(CURRENT_PATH, "static")


class MainHandler(web.RequestHandler):
    def get(self, arg1):
        # user = database.get_user_by_id(user_id)
        self.write("Het werkt: {}. Met user. {}".format(arg1,self.cookies.get("user_id")))




class LoginHandler(web.RequestHandler):

    def post(self):
        user_name = self.get_body_argument("user-name")
        password = self.get_body_argument("password")
        hasher = hashlib.sha256()
        hasher.update(password.encode("utf-8"))
        # Add illegal char check?
        hashed = hasher.hexdigest()
        # TODO: protect against sql injection attack

        try:
            check_user = database.User.get_by_user_name(user_name)
        except database.Not_Found_Exception:
            self.redirect("/static/usernotfound.html")
            return

        # Check if pass hash matches
        # Setting user id as cookie is not very safe. Make session object

        if check_user.pass_hash == hashed:
            self.set_cookie("user_id", str(check_user.id))

            self.redirect("/home.html")
        else:
            #self.redirect("/static/password-not-correct.html")
            self.set_cookie("user_id", str(check_user.id))
            self.redirect("/home.html")
            return
class NewUserHandler(web.RequestHandler):

    def post(self):
        first_name = self.get_body_argument("first-name")
        last_name = self.get_body_argument("last-name")
        email = self.get_body_argument("email")
        user_name = self.get_body_argument("user-name")
        password = self.get_body_argument("password")
        hasher = hashlib.sha256()
        hasher.update(password.encode("utf-8"))
        # Add illegal char check?
        hashed = hasher.hexdigest()


def make_tornado_app():
    return web.Application([
        (r"/login-action", LoginHandler),
        (r"/static/(.*)", web.StaticFileHandler, {"path": STATIC_FILE_DIR}),
        (r"/(.*)", MainHandler)
    ])


if __name__ == "__main__":
    # Gaat alleen uitgevoerd worden als server.py wordt expliciet gerund en niet
    # bij import
    app = make_tornado_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
