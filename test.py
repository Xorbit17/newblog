from database import Database
import model
import util
import blog_types

db = Database("sqlite:///user.db")
db.create_schema(model.Base)

session = db.get_session()


# Query dennis
new_dennis = session.query(model.User).filter_by(user_name="sdfas").first()  # type: model.User
print(new_dennis)
session.close()
