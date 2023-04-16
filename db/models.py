

from sqlalchemy import inspect
from sqlalchemy import String, BigInteger

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, )
    prefix: Mapped[str] = mapped_column(String(15))
    group_id: Mapped[int] = mapped_column(nullable=True)
    teacher_id: Mapped[str] = mapped_column(String(5), nullable=True)

    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in mapper.column_attrs:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"
