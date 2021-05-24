import asyncio
import config
import multiprocessing
import sys
import time

from app.database.migrations import migrate_db
from app.discord import discord_bot
from app.service.Log import Log


#TIMER
start_time = time.time()
buffer_time = 10 * 60 # 15 minutes
exit_after = 24 * 60 * 60 # 24 hours in second

def initApp():
    # Initiate logger service
    Log(discord_bot)

    # Migrate database
    asyncio.run(migrate_db())

    # Start discord bot
    discord_bot.run(config.DISCORD_TOKEN)
    

# TODO: delete later
if __name__ == '__main__':
    p = multiprocessing.Process(target=initApp, name="initApp")
    p.start()

    #Timer
    while(time.time() - start_time <= (exit_after - buffer_time)):
        time.sleep(10 * 60) #sleep every 10 mins

    #Exit program after timer end
    p.terminate()
    p.join()
    sys.exit()

