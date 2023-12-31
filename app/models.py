from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# This piece of code initializes the table - Describes how the table will look like at Postgresql

class Post(Base):
    __tablename__ = 'user_posts'

    id = Column (Integer, primary_key = True, nullable = False)
    title = Column (String, nullable = False)
    content = Column (String, nullable = False)
    published = Column(Boolean, server_default = "TRUE", nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default =  text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable =False)
    
class Users(Base):
    __tablename__ = 'users'

    id = Column (Integer, primary_key = True, nullable = False)
    email = Column (String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default =  text('now()'))

class Votes(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("user_posts.id", ondelete="CASCADE"), primary_key = True)
    