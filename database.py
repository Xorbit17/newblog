import sqlite3

conn = sqlite3.connect('user.db')


class Not_Found_Exception(Exception):
    pass


def exec_sql_fetchone(sql):
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchone()
    if result is None:
        raise Not_Found_Exception()
    c.close()
    conn.commit()
    return result


def exec_sql(sql):
    c = conn.cursor()
    c.execute(sql)
    last_row = c.lastrowid
    c.close()
    conn.commit()

    return last_row


class User(object):
    def __init__(self):
        self.id = -1
        self.first_name = ""
        self.last_name = ""
        self.user_name = ""
        self.email = ""
        self.pass_hash = ""

    def save_to_db(self):
        if self._check_if_exists_user_name():
            self._update()
        else:
            self._new_commit()


    def _check_if_exists_user_name(self):
        sql = "SELECT Count(*) FROM User WHERE user_name=\"{}\"".format(self.user_name)
        return exec_sql_fetchone(sql)[0] == 1

    def _update(self):
        sql = "UPDATE User SET " \
              "first_name=\"{}\", " \
              "last_name=\"{}\", " \
              "user_name=\"{}\", " \
              "email=\"{}\", " \
              "pass_hash=\"{}\" " \
              "WHERE ID={}".format(self.first_name, self.last_name, self.user_name, self.email, self.pass_hash, self.id)
        exec_sql(sql)

    def _new_commit(self):
        sql = "INSERT INTO User VALUES (NULL, \"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(
            self.first_name,
            self.last_name,
            self.user_name,
            self.email,
            self.pass_hash
        )

        self.id = exec_sql(sql)

    @staticmethod
    def _copy_result_to_user(result):
        new_user = User()
        new_user.id = result[0]
        new_user.first_name = result[1]
        new_user.last_name = result[2]
        new_user.user_name = result[3]
        new_user.email = result[4]
        new_user.pass_hash = result[5]

        return new_user

    @staticmethod
    def count():
        result = exec_sql_fetchone("SELECT COUNT(*) FROM User")
        return int(result[0])

    @staticmethod
    def get_by_id(user_id):
        result = exec_sql_fetchone("SELECT * FROM User WHERE id={}".format(user_id))
        return User._copy_result_to_user(result)

    @staticmethod
    def get_by_user_name(user_name):
        result = exec_sql_fetchone("SELECT * FROM User WHERE user_name=\"{}\"".format(user_name))
        return User._copy_result_to_user(result)


def get_user_by_id(id: int):
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE id={}".format(id))
    result = c.fetchone()
    c.close()
    return result
