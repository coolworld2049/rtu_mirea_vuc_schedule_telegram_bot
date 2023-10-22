import sqlalchemy as sa
from sqlalchemy import Column, BigInteger, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from telegram_bot.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    __created_at_name__ = "created_at"
    __updated_at_name__ = "updated_at"
    __datetime_func__ = sa.func.now()

    created_at = sa.Column(
        __created_at_name__,
        sa.TIMESTAMP(timezone=True),
        default=__datetime_func__,
        nullable=True,
    )

    updated_at = sa.Column(
        __updated_at_name__,
        sa.TIMESTAMP(timezone=True),
        default=__datetime_func__,
        onupdate=__datetime_func__,
        nullable=True,
    )


class User(BaseModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String(128))
    full_name = Column(String(128))
    user_settings = relationship("UserSettings", backref="users")


class UserSettings(BaseModel):
    __tablename__ = "user_settings"

    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    platoon = Column(SmallInteger)
    course = Column(SmallInteger)
