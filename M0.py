import aiosqlite
from aiohttp import web
from OuterFunc import RowFetcher, AddToDB

async def create_database():
    async with aiosqlite.connect("baza.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS baza (
                id INTEGER PRIMARY KEY,
                username TEXT,
                ghublink TEXT,
                filename TEXT,
                content TEXT
            )
        ''')
        await db.commit()

async def check_and_fill_database():
    async with aiosqlite.connect("baza.db") as db:
        async with db.execute("SELECT COUNT(*) FROM baza") as cursor:
            async for row in cursor:
                if row[0] == 0:
                    print("Database is empty. Filling with fake data.")
                    await AddToDB(db)  # Pass the db connection as an argument
                else:
                    print("Database is not empty.")

async def json_data(request):
    try:
        await create_database()
        await check_and_fill_database()

        async with aiosqlite.connect("baza.db") as db:
            data = await RowFetcher(db)
            return web.json_response(
                {
                    "name": "service0",
                    "status": "OK",
                    "message": "Successfully added to the database",
                    "data": data,
                },
                status=200,
            )
    except Exception as e:
        return web.json_response({"name": "service0", "error": str(e)}, status=500)

app = web.Application()
app.router.add_get("/", json_data)
web.run_app(app, port=8080)