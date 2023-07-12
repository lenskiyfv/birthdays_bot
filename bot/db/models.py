from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)


class Birthday(Base):
    __tablename__ = "birthday"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    user_id = Column(
        BigInteger, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )

    users = relationship(User, backref="birthday")


async def init_models(engine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
