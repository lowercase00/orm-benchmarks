import asyncio
import os
import time
from random import choice

from models import Journal, async_session, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))


async def test():
    async with async_session() as session:

        session.bulk_save_objects(
            [
                Journal(level=choice(LEVEL_CHOICE), text=f"Insert from C, item {i}")
                for i in range(count)
            ]
        )
        await session.commit()


start = now = time.time()
asyncio.run(test())
now = time.time()

print(f"SQLAlchemy ORM, C: Rows/sec: {count / (now - start): 10.2f}")
