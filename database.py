import aiosqlite

DB_PATH = "trivia.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                guild_id INTEGER NOT NULL,
                user_id  INTEGER NOT NULL,
                points   INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
        """)
        await db.commit()


async def add_point(guild_id, user_id, amount=1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO scores (guild_id, user_id, points) VALUES (?, ?, ?)
            ON CONFLICT(guild_id, user_id)
            DO UPDATE SET points = points + excluded.points
        """, (guild_id, user_id, amount))
        await db.commit()


async def get_top(guild_id, limit=10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT user_id, points FROM scores
            WHERE guild_id = ?
            ORDER BY points DESC
            LIMIT ?
        """, (guild_id, limit)) as cursor:
            return await cursor.fetchall()


async def get_score(guild_id, user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT points FROM scores WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
