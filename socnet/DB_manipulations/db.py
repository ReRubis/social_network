import datetime
import uuid

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Identity,
                        Integer, String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base(object):
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
