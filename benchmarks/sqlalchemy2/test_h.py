import asyncio
import os
import time

from models import Journal, async_session, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))


Session = sessionmaker(bind=engine)

start = time.time()
session = Session()
count = 0

for _ in range(10):



async def test():
    async with async_session() as session:

        for _ in range(10):
            for level in LEVEL_CHOICE:
                res = list(
                    session.query(Journal)
                    .filter(Journal.level == level)
                    .with_entities(*Journal.__table__._columns)
                )
                count += len(res)


start = time.time()
asyncio.run(test())
now = time.time()


print(f"SQLAlchemy ORM, H: Rows/sec: {count / (now - start): 10.2f}")
