import asyncio
import os
import time
from random import randint

from models import Journal, async_session, engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))
maxval = count - 1
count *= 2


async def test():
    async with async_session() as session:

        for _ in range(count):
            query = select(Journal).where(Journal.id == randint(1, maxval))
            results = await session.execute(query)
            res = results.scalars().all()


start = time.time()
asyncio.run(test())
now = time.time()

print(f"SQLAlchemy ORM, F: Rows/sec: {count / (now - start): 10.2f}")
