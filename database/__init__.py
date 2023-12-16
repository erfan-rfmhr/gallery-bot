import aiosqlite


async def create_db():
    async with aiosqlite.connect('bot.db') as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            isSent BOOLEAN DEFAULT FALSE
        )
        ''')
        await db.execute('''
        CREATE TABLE IF NOT EXISTS public_hashtags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag VARCHAR(255) NOT NULL
        )
        ''')
        await db.commit()
