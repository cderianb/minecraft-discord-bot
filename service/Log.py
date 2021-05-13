import os
import time

class Log():
    def __init__(self, bot, channel_id):
        self.channel = bot.get_channel(channel_id)

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
        await self.channel.send(msg)
    
    def __print_to_log_file(self, msg):
        with open('err.log', 'a') as f:
            f.write(f"{msg}\n")



    
