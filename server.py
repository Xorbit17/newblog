import tornado.web as web
import tornado.ioloop as ioloop
import os
import hashlib
import database  # Hier wordt code uitgevoerd!!
import re

import model

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_FILE_DIR = os.path.join(CURRENT_PATH, "static")

USER_REGEX = r"^(?=.{2,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
PASS_REGEX = r"^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"

user_regex_compiled = re.compile(USER_REGEX)
pass_regex_compiled = re.compile(PASS_REGEX)


class MainHandler(web.RequestHandler):
    """This wil process templates"""

    def get(self, arg1):
        # user = database.get_user_by_id(user_id)
        self.write("Het werkt: {}. Met user. {}".format(arg1, self.cookies.get("user_id")))

        dennis = model.User()
        dennis.user_name = "dve"


class LoginHandler(web.RequestHandler):
    """Handles login form request with a body"""

    def post(self):
        user_name = self.get_body_argument("user-name")
        password = self.get_body_argument("password")
        # Bevatten user name en paswoord geen stoute dingen?
        if user_regex_compiled.match(user_name) is None:
            self.redirect("/static/login.html?err=user%20not%20ok")
            return
        if pass_regex_compiled.match(password) is None:
            self.redirect("/static/login.html?err=pass%20not%20ok")
            return

        hasher = hashlib.sha256()
        hasher.update(password.encode("utf-8"))
        # Add illegal char check?
        hashed = hasher.hexdigest()

        try:
            check_user = database.User.get_by_user_name(user_name)
        except database.Not_Found_Exception:
            self.redirect("/static/login.html?err=user%20not%20found")  # html file aangemaakt maar moet nog uitbreiden
            return

        # Check if pass hash matches
        # Setting user id as cookie is not very safe. Make session object

        if check_user.pass_hash == hashed:
            self.set_cookie("user_id", str(check_user.id))
            self.redirect("/home.html")
        else:
            # self.redirect("/static/password-not-correct.html")
            # self.redirect("/static/login.html?err=pass%20not%20correct") #snel een html file aangemaakt!

            self.set_cookie("user_id", str(check_user.id))
            self.redirect("/home.html")  # home.html of static.html????
            return


"""
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
        new_user = database.User()
        new_user.first_name = first_name
        new_user.last_name_name = last_name
        new_user.email = email
        new_user.password = hashed
        new_user.user_name = user_name
        new_user.save_to_db()
        self.redirect("/static/login.html")
"""


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
