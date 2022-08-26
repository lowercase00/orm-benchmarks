import asyncio
import os
import time
from random import randrange

from models import Journal, async_session, engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get("ITERATIONS", "1000"))


count = 0


async def test():
    async with async_session() as session:
        for _ in range(iters // 10):
            for level in LEVEL_CHOICE:
                query = (
                    select(Journal)
                    .where(Journal.level == level)
                    .limit(20)
                    .offset(randrange(iters - 20))
                )
                res = await session.execute(query)
                count += len(res.scalars().all())


start = time.time()
asyncio.run(test())
now = time.time()

print(f"SQLAlchemy ORM, E: Rows/sec: {count / (now - start): 10.2f}")
