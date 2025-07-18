import aiomysql

class Database:
    def __init__(self, conf):
        self.conf = conf
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.conf['host'],
            user=self.conf['user'],
            password=self.conf['password'],
            db=self.conf['database']
        )

    async def get_balance(self, user_id, coin):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT balance FROM balances WHERE user_id=%s AND coin=%s", (str(user_id), coin))
                r = await cur.fetchone()
                return r[0] if r else 0.0

    async def update_balance(self, user_id, coin, amount):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO balances (user_id, coin, balance) VALUES (%s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE balance = balance + %s",
                    (str(user_id), coin, amount, amount)
                )
                await conn.commit()
