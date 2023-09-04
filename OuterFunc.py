import aiohttp
import numpy as np
import pandas as pd

async def RowFetcher(db):
	cursor = await db.cursor()
	await cursor.execute("SELECT COUNT(*) FROM baza")
	(RowNumber,) = await cursor.fetchone()
	RandomRowIndex = np.random.randint(0, RowNumber, size = 100)
	rows = []
	for rowIndex in RandomRowIndex:
		await cursor.execute("SELECT * FROM baza LIMIT 1 OFFSET %s"%(rowIndex))
		rows.append(await cursor.fetchone())
	return rows

async def WorkerTokenizer(URL, data):
	for index in range(len(data)):
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			async with session.post(URL, json = data[index]) as response:
				WTResponse = await response.json()
	return WTResponse

async def ForwardToService4(data):
	async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
		async with session.post("http://localhost:8084/gatherData", json = data) as response:
			Service4Response = await response.json()
	return Service4Response

async def AddToDB(db):
    try:
        df = pd.read_json('FakeDataset.json', lines=True)
        for index, row in df.tail(10000).iterrows():
            await db.execute(
                "INSERT INTO baza (username, ghublink, filename, content) VALUES (?, ?, ?, ?)",
                (
                    row.get("repo_name").split("/", 1)[0],
                    "https://github.com/" + row.get("repo_name"),
                    row.get("path").rsplit("/", 1)[1],
                    row.get("content")
                )
            )
            await db.commit()
        print("Data successfully added to the database.")
    except Exception as e:
        print("An error occurred:", e)