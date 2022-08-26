import asyncio
import os
import time

from models import Journal, async_session, engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))


count = 0


async def test():
    async with async_session() as session:

        for _ in range(10):
            for level in LEVEL_CHOICE:
                res = [
                    {k: v for k, v in value.__dict__.items() if k[:4] != "_sa_"}
                    for value in session.query(Journal).filter(Journal.level == level)
                ]
                count += len(res)


start = time.time()
asyncio.run(test())
now = time.time()


print(f"SQLAlchemy ORM, G: Rows/sec: {count / (now - start): 10.2f}")
