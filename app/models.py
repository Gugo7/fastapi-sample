from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text



class Post(Base):
    __tablename__ = 'posts'

    #Columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    published = Column(Boolean, server_default='False')
    edited = Column(Boolean, server_default='False')
    edited_at = Column(TIMESTAMP(timezone=True), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('User')



class User(Base):
    __tablename__ = 'users'

    #Columns
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number =Column(String)



class Vote(Base):
    __tablename__ = 'votes'

    #Columns
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True) 
