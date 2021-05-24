from app.database.provider.PostgreSQL import postgre
from app.service.Log import Log

query = [
    "CREATE TABLE IF NOT EXISTS dead(id SERIAL PRIMARY KEY, player varchar(50), days int, reason varchar(50), time date NOT NULL);",
    "SET timezone TO 'Asia/Jakarta';",
    "ALTER TABLE dead ADD COLUMN IF NOT EXISTS time date;",
    """CREATE TABLE IF NOT EXISTS coordinates(
    id SERIAL PRIMARY KEY, 
    description varchar(100),
    x smallint, 
    y smallint, 
    z smallint
    );"""
]

async def migrate_db():
    Logger = Log()
    for q in query:
        try:
            await postgre.get().execute(q)
        except Exception as e:
            q_log = f"```{q}```"
            await Logger.warn(f"Failed to execute query {q_log} due to {e}")