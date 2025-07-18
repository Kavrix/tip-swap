import aiomysql


class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None

    async def init_pool(self):
        """Initialize the connection pool to MySQL."""
        self.pool = await aiomysql.create_pool(
            host=self.config.mysql_host,
            port=self.config.mysql_port,
            user=self.config.mysql_user,
            password=self.config.mysql_password,
            db=self.config.mysql_database,
            autocommit=True,
            minsize=1,
            maxsize=10
        )
        print("✅ MySQL connection pool created.")

    async def execute(self, query, args=None):
        """Execute a query (INSERT/UPDATE/DELETE)."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                await conn.commit()

    async def fetch(self, query, args=None):
        """Fetch multiple rows from the database."""
        async with self.pool.acquire() as conn:
            asy
