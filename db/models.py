

from typing import Optional

from sqlalchemy import inspect
from sqlalchemy import String, BigInteger, SmallInteger, DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    prefix: Mapped[str] = mapped_column(String(25))
    group_id: Mapped[int] = mapped_column(nullable=True)
    teacher_id: Mapped[str] = mapped_column(String(5), nullable=True)
    office_id: Mapped[int] = mapped_column(SmallInteger())
    last_interaction = mapped_column(DateTime())

    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in mapper.column_attrs:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


class Office(Base):
    __tablename__ = "offices"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str]

    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in mapper.column_attrs:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in mapper.column_attrs:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    currator: Mapped[Optional[str]] = mapped_column(nullable=True)

    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in mapper.column_attrs:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"
