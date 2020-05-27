import tornado.web as web
import tornado.ioloop as ioloop
import os
import hashlib
import database  # Hier wordt code uitgevoerd!!
import re

import model
import util

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_FILE_DIR = os.path.join(CURRENT_PATH, "static")
TEMPLATE = os.path.join(CURRENT_PATH, "templates")

USER_REGEX = r"^(?=.{2,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
PASS_REGEX = r"^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"

user_regex_compiled = re.compile(USER_REGEX)
pass_regex_compiled = re.compile(PASS_REGEX)

db = database.Database(database_connection_string="sqlite:///user.db")


class MainHandler(web.RequestHandler):
    """This wil process templates"""

    def get(self, arg1):
        # self.render("home.html", title="Homepage")
        if arg1 == "":
            arg1 = "home.html"
        self.render(arg1, title="Homepage")
        # user = database.get_user_by_id(user_id)
        # self.write("Het werkt: {}. Met user. {}".format(arg1, self.cookies.get("user_id")))
        # er klopt hier iets niet!


class LoginHandler(web.RequestHandler):
    """Handles login form request with a body"""

    # GEEN GET

    def post(self):
        user_name = self.get_body_argument("user-name")
        password = self.get_body_argument("password")
        # Bevatten user name en paswoord geen stoute dingen?
        if user_regex_compiled.match(user_name) is None:
            self.redirect("login.html?err=user%20not%20ok")  # Status 3XX
            return
        """
        if pass_regex_compiled.match(password) is None:
            self.redirect("login.html?err=pass%20not%20ok")
            return
        """

        hashed = util.plaintext_to_hash(password)

        session = db.get_session()

        check_user = session.query(model.User).filter_by(user_name=user_name).first()  # type:model.User
        if check_user is None:  # Not found
            self.redirect("login.html?err=user%20not%20found")
            return

        # Check if pass hash matches
        # Setting user id as cookie is not very safe. Make state object

        if check_user.pass_hash == hashed:
            # Pass is ok
            self.set_cookie("user_id", str(check_user.id))
            self.redirect("home.html")
        else:
            # pass is not ok
            self.redirect("login.html?err=pass%20not%20correct")
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
        self.redirect("/templates/login.html")
"""


def make_tornado_app():
    return web.Application([
        (r"/login-action", LoginHandler),
        (r"/static/(.*)", web.StaticFileHandler, {"path": STATIC_FILE_DIR}),
        (r"/(.*)", MainHandler)
    ], template_path=TEMPLATE)


if __name__ == "__main__":
    # Gaat alleen uitgevoerd worden als server.py wordt expliciet gerund en niet
    # bij import
    app = make_tornado_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
