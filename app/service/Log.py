import config
import time

from app.core.Singleton import Singleton

class Log(metaclass=Singleton):
    def __init__(self, bot):
        self.channel = bot.get_channel(config.DEV_CHANNEL_ID)

    async def warn(self, msg):
        warn_msg = f"[WARN] [{time.asctime()}] {msg}"
        self.__print_to_log_file(warn_msg)
        await self.__send_to_channel(warn_msg)

    async def info(self, msg):
        info_msg = f"[INFO] [{time.asctime()}] {msg}"
        self.__print_to_log_file(info_msg)
    
    async def error(self, msg):
        error_msg = f"[ERROR] [{time.asctime()}] {msg}"
        self.__print_to_log_file(error_msg)
        await self.__send_to_channel(error_msg)

    async def __send_to_channel(self, msg):
        # await self.channel.send(msg)
        pass
    
    def __print_to_log_file(self, msg):
        with open('err.log', 'a') as f:
            f.write(f"{msg}\n")
