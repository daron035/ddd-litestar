import asyncio

import asyncpg


async def test_connection():
    conn = await asyncpg.connect(user="admin", password="admin", database="postgres_db", host="127.0.0.1", port=15432)
    print("Connected successfully!")
    await conn.close()


asyncio.run(test_connection())
