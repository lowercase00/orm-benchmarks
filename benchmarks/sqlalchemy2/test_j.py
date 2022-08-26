import asyncio
import os
import time
from random import choice

from models import Journal, async_session, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))


objs = list(session.query(Journal).all())
count = len(objs)


async def test():
    async with async_session() as session:

        for obj in objs:
            obj.level = choice(LEVEL_CHOICE)
            session.add(obj)
        await session.commit()


start = time.time()
asyncio.run(test())
now = time.time()

print(f"SQLAlchemy ORM, J: Rows/sec: {count / (now - start): 10.2f}")
