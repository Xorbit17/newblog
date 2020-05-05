import blog_types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

"""This module contains simple objects modeling what we need in order to make the blog work"""

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    user_name = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    pass_hash = Column(String)
    role = Column(Enum(blog_types.Role), default=blog_types.Role.VISITOR)

    def __repr__(self):
        return "<User(user_name={},email={})>".format(self.user_name, self.email)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    reference = Column(String, unique=True)
    body = Column(String)
    keywords = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship("User", back_populates="articles")


User.articles = relationship("Article", order_by=Article.id, back_populates="author")
