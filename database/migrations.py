from database.provider.PostgreSQL import postgre

query = [
    "CREATE TABLE IF NOT EXISTS dead(id SERIAL PRIMARY KEY, player varchar(50), days int, reason varchar(50), time date NOT NULL);",
    "SET timezone TO 'Asia/Jakarta';",
    "ALTER TABLE dead ADD COLUMN IF NOT EXISTS time date;",
    """CREATE TABLE IF NOT EXISTS coordinates(
	id SERIAL PRIMARY KEY, 
    description varchar(100),
	x smallint, 
	y smallint, 
	z smallint,
    );"""
]

async def migrate_db():
    for q in query:
        # Maybe add log?
        await postgre.get().execute(q)