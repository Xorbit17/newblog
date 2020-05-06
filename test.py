from database import Database
import model
import util
import blog_types

db = Database("sqlite:///user.db")
db.create_schema(model.Base)

session = db.get_session()

# Add dennis
dennis = model.User(first_name="Dennis",
                    last_name="Van Eecke",
                    user_name="dve",
                    email="dennis.vaneecke@gmail.com",
                    pass_hash=util.plaintext_to_hash("0mg-Pr@tput!"),
                    role=blog_types.Role.ADMIN)

session.add(dennis)

session.commit()

# Query dennis
new_dennis = session.query(model.User).filter_by(user_name="dve").first()  # type: model.User
if dennis is new_dennis:
    print("Got the same instance")
print("Role of dennis: " + new_dennis.role.name)

# Change dennis
dennis.email = "sinterklaas@telenet.be"
session.commit()

#Delete dennis
session.query(model.User).filter_by(user_name="dve").delete(synchronize_session=False)
session.commit()


session.close()
