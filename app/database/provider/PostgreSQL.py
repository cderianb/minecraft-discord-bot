import os
import asyncpg
from app.core.Singleton import Singleton

class PostgreSQL(metaclass=Singleton):
    def __init__(self):
        self.db = None

    def __get_credentials(self):
        return {
            "user": os.getenv('POSTGRES_USER'), 
            "password": os.getenv('POSTGRES_PASSWORD'), 
            "database": os.getenv('POSTGRES_DATABASE'), 
            "host": os.getenv('POSTGRES_HOST')
        }
    
    async def connect(self):
        self.db = await asyncpg.create_pool(**self.__get_credentials())
    
    async def disconnect(self):
        await self.db.close()

    def get(self):
        return self.db

postgre = PostgreSQL()