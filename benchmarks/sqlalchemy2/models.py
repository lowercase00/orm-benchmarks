import os
from datetime import datetime
from decimal import Decimal
from typing import Callable

from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    SmallInteger,
    String,
    Text,
    create_engine,
    event,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    Session,
    close_all_sessions,
    declarative_base,
    registry,
    relationship,
    scoped_session,
    sessionmaker,
)
from sqlalchemy.pool import NullPool

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    async_engine = create_async_engine(
        f"postgresql+asyncpg://postgres:{os.environ.get('PASSWORD')}@localhost/tbench"
    )
elif dbtype == "mysql":
    async_engine = create_async_engine(
        f"mysql+aiomysql://root:{os.environ.get('PASSWORD')}@localhost/tbench"
    )
else:
    async_engine = create_engine("sqlite+aiosqlite:////tmp/db.sqlite3")

Base = declarative_base()


async_session: Callable[..., AsyncSession] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(Base):
        __tablename__ = "journal"

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now, nullable=False)
        level = Column(SmallInteger, index=True, nullable=False)
        text = Column(String(255), index=True, nullable=False)


if test == 2:

    class JournalRelated(Base):
        __tablename__ = "journal_related"
        journal_id = Column(Integer, ForeignKey("journal.id"), primary_key=True)
        journal_from_id = Column(Integer, ForeignKey("journal.id"), primary_key=True)

    class Journal(Base):
        __tablename__ = "journal"

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now, nullable=False)
        level = Column(SmallInteger, index=True, nullable=False)
        text = Column(String(255), index=True, nullable=False)
        parent_id = Column(Integer, ForeignKey("journal.id"))
        parent = relationship("Journal", remote_side=id, backref="children")
        related = relationship(
            "JournalRelated", backref="to", primaryjoin=id == JournalRelated.journal_id
        )
        related_from = relationship(
            "JournalRelated",
            backref="from",
            primaryjoin=id == JournalRelated.journal_from_id,
        )


if test == 3:

    class Journal(Base):
        __tablename__ = "journal"

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, default=datetime.now, nullable=False)
        level = Column(SmallInteger, index=True, nullable=False)
        text = Column(String(255), index=True, nullable=False)

        col_float1 = Column(Float, default=2.2, nullable=False)
        col_smallint1 = Column(SmallInteger, default=2, nullable=False)
        col_int1 = Column(Integer, default=2000000, nullable=False)
        col_bigint1 = Column(BigInteger, default=99999999, nullable=False)
        col_char1 = Column(String(255), default="value1", nullable=False)
        col_text1 = Column(
            Text,
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
            nullable=False,
        )
        col_decimal1 = Column(Numeric(12, 8), default=Decimal("2.2"), nullable=False)
        col_json1 = Column(
            JSON,
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
            nullable=False,
        )

        col_float2 = Column(Float)
        col_smallint2 = Column(SmallInteger)
        col_int2 = Column(Integer)
        col_bigint2 = Column(BigInteger)
        col_char2 = Column(String(255))
        col_text2 = Column(Text)
        col_decimal2 = Column(Numeric(12, 8))
        col_json2 = Column(JSON)

        col_float3 = Column(Float, default=2.2, nullable=False)
        col_smallint3 = Column(SmallInteger, default=2, nullable=False)
        col_int3 = Column(Integer, default=2000000, nullable=False)
        col_bigint3 = Column(BigInteger, default=99999999, nullable=False)
        col_char3 = Column(String(255), default="value1", nullable=False)
        col_text3 = Column(
            Text,
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa",
            nullable=False,
        )
        col_decimal3 = Column(Numeric(12, 8), default=Decimal("2.2"), nullable=False)
        col_json3 = Column(
            JSON,
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True},
            nullable=False,
        )

        col_float4 = Column(Float)
        col_smallint4 = Column(SmallInteger)
        col_int4 = Column(Integer)
        col_bigint4 = Column(BigInteger)
        col_char4 = Column(String(255))
        col_text4 = Column(Text)
        col_decimal4 = Column(Numeric(12, 8))
        col_json4 = Column(JSON)


async def create_tables():
    async with async_session() as session:
        session.run_sync(Base.metadata.create_all(async_engine))
