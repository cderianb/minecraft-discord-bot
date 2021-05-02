# https://crt.sh/?id=2835394 -> SSL Certificate if needed
import os
import random
import discord
import asyncpg

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
#Bot Credential
TOKEN = os.getenv('DISCORD_TOKEN')  #token untuk connect ke bot nya
GUILD = os.getenv('DISCORD_GUILD')

#Database Credential
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

bot = commands.Bot(command_prefix='!')

# Change to object Bot
db = None

@bot.event
async def on_ready():
    credentials = {"user": f"{POSTGRES_USER}", 
                    "password": f"{POSTGRES_PASSWORD}", 
                    "database": f"{POSTGRES_DATABASE}", 
                    "host": f"{POSTGRES_HOST}"}

    global db # ganti jadi object sendiri, jangan pake global
    db = await asyncpg.create_pool(**credentials)
    await db.execute("CREATE TABLE IF NOT EXISTS dead(id SERIAL PRIMARY KEY, player varchar(50), days int, reason varchar(50));")
    print(f'{bot.user.name} has connected to discord')


@bot.event
async def on_command_error(ctx, error):
    with open('err.log', 'a') as f:
        f.write(f'Unhandled Exception: {error}\n')
    await ctx.send('Error occured. Contact administrator.')


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return  # kalo dapet message dari bot diri sendiri abaikan

    if message.content.startswith('!'):
        await bot.process_commands(message)  # kalo dapet command (awalan !)
        return 

@bot.command(name='mc-death', help='mc-death [player] [day_count] [reason]')
async def mc_death(ctx, *message):
    
    connection = await db.acquire()
    async with connection.transaction():
        query = f'INSERT INTO dead(player, days, reason) VALUES($1, $2, $3);'
        await db.execute(query, message[0], int(message[1]), message[2])
    await db.release(connection)

    await ctx.send('Stats Updated')

@bot.command(name='mc-history', help='see current death stats')
async def mc_history(ctx, *message):
    embed_message = discord.Embed(title="Minecraft Hardcore Death History", description="Death History", color=0x00ff00)

    query = "SELECT * FROM dead;"
    rows = await db.fetch(query) # return list of all row
    message = """
+-------------------+-------------------+-------------------+
|       Player      |        Days       |       Reason      |
+-------------------+-------------------+-------------------+\n"""
    for row in rows:
        message += f'|{row[1].center(19)}|{(str(row[2])).center(19)}|{row[3].center(19)}|\n'
    message += '+-------------------+-------------------+-------------------+\n'
    embed_message.add_field(name="History", value=f"```{message}```", inline=True)
    await ctx.send(embed=embed_message)

@bot.command(name='mc-stats', help='see current death stats')
async def mc_stats(ctx, *message):
    embed_message = discord.Embed(title="Minecraft Hardcore Dead Stats", description="Death Counter", color=0x00ff00)
    
    query = "select player, count(*) from dead group by player ORDER BY 2 DESC, 1;"
    rows = await db.fetch(query)
    message = """
+--------------------+--------------------+
|       Player       |        Score       |
+--------------------+--------------------+\n"""
    for row in rows:
        message += f'|{row[0].center(20)}|{(str(row[1])).center(20)}|\n'
    message += '+--------------------+--------------------+\n'
    embed_message.add_field(name="Stats", value=f"```{message}```", inline=True)
    await ctx.send(embed=embed_message)

bot.run(TOKEN)  #connect ke bot nya