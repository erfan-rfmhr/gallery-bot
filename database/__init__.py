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
        await db.commit()
