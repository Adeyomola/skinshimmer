from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Text, ForeignKey, NVARCHAR, Boolean
import datetime

def metadata():
    md = MetaData()

    users = Table(
    'users', md, 
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('username', String(255), unique=True),
    Column('password', String(255)),
    Column('email', String(255), unique=True),
    Column('image_url', NVARCHAR(255))
        )
    post = Table(
    'post', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('author_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('firstname', String(255)),
    Column('created', TIMESTAMP, default=datetime.datetime.now),
    Column('title', Text, nullable=False, unique=True),
    Column('body', Text, nullable=False),
    Column('image_url', NVARCHAR(255)),
    Column('category', Text, nullable=False)
    )
    comments = Table(
    'comments', md,
    Column('post', Integer),
    Column('name', Text, nullable=False),
    Column('comment', Text, nullable=False, unique=True),
    )
    return md