from database.provider.PostgreSQL import postgre

async def rename_player(name: str, id: str):
    connection = await postgre.get().acquire()
    async with connection.transaction():
        query = f'UPDATE dead SET player=$1 WHERE player=$2;'
        await postgre.get().execute(query, id, name)
    await postgre.get().release(connection)

async def update_player_death(id: str, day: int, reason: str, _time: str = None):
    time = _time if _time != None else "NOW()"
    connection = await postgre.get().acquire()
    async with connection.transaction():
        query = f'INSERT INTO dead(player, days, reason, time) VALUES($1, $2, $3, {time});'
        await postgre.get().execute(query, id, day, reason)
    await postgre.get().release(connection)

async def get_all_player_dead_history(offset: int, limit: int = 10):
    query = f"SELECT * FROM dead ORDER BY id DESC LIMIT {limit} OFFSET {offset};"
    return await postgre.get().fetch(query)

async def get_player_dead_history(id: int, offset: int, limit = 10):
    query = f"SELECT days, reason, time FROM dead WHERE player = '{id}' ORDER BY id DESC LIMIT {limit} OFFSET {offset};"
    return await postgre.get().fetch(query)

async def get_death_stats():
    query = "select player, count(*) from dead group by player ORDER BY 2 DESC, 1 LIMIT 10;"
    return await postgre.get().fetch(query)

async def insert_landmark(x:int, y:int, z:int, description:str):
    connection = await postgre.get().acquire()
    async with connection.transaction():
        query = f'INSERT INTO coordinates(x, y, z, description) VALUES($1, $2, $3, $4);'
        await postgre.get().execute(query, x, y, z, description)
    await postgre.get().release(connection)

async def update_landmark():
    return NotImplementedError()

async def delete_landmark():
    return NotImplementedError()

async def get_all_coordinates(offset: int, limit: int = 10):
    query = f"SELECT * FROM coordinates ORDER BY id DESC LIMIT {limit} OFFSET {offset};"
    return await postgre.get().fetch(query)