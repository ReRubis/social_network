import datetime
import uuid

from sqlalchemy import (Column, DateTime, ForeignKey,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.sql import func

_Base = declarative_base()


class Base(_Base):
    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    removed_at = Column(DateTime(timezone=True))


class User(Base):

    username = Column(String, nullable=False, unique=True)
    hashedpassword = Column(String, nullable=False)


class Post(Base):

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    text = Column(String)


class Reaction(Base):

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id'))
    reaction = Column(String, nullable=False)
    # Currently supports only 'like' and 'dlike'
