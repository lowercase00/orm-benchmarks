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
                query = select(Journal).where(Journal.level == level)
                results = await session.execute(query)
                resp = list(results.scalars().all())
                count += len(resp)


start = time.time()
asyncio.run(test())
now = time.time()

print(f"SQLAlchemy ORM, D: Rows/sec: {count / (now - start): 10.2f}")
