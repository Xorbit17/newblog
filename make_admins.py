from database import Database
import model
import util
import blog_types

db = Database("sqlite:///user.db")

session = db.get_session()

new_dennis = model.User(first_name="Dennis",
                        last_name="Van Eecke",
                        user_name="dve",
                        email="dennis.vaneecke@gmail.com",
                        pass_hash=util.plaintext_to_hash("0mg-Pr@tput!"),
                        role=blog_types.Role.ADMIN)

new_djamilla = model.User(first_name="Djamilla",
                          last_name="Simoens",
                          user_name="dj",
                          email="djamill.simoens@gmail.com",
                          pass_hash=util.plaintext_to_hash("Wh@ev3r-Pasw00rd!"),
                          role=blog_types.Role.ADMIN)

dennis = session.query(model.User).filter_by(user_name="dve").first()  # type:model.User
if dennis is None:
    session.add(new_dennis)
else:
    print("Dennis already exists: {}".format(dennis))

djamilla = session.query(model.User).filter_by(user_name="dj").first()
if djamilla is None:
    session.add(new_djamilla)
else:
    print("Djamilla already exists: {}".format(djamilla))

session.commit()
session.close()

db.dispose()
