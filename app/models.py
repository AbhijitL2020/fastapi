from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):                   # class Post extends Base
    __tablename__ = "posts"         # This was smposts, and that created a problem in alembic autogenerate!

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")                            # Added while learning relationship

class User(Base):                       # user table
    __tablename__ = "users"             # SQLAlchemy only checks whether the table is present. if not, creates the tables. BUT NO UPDATES

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),  primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),  primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

