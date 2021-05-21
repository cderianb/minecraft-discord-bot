from module.minecraft import constant
import discord
import requests
import os
import math
import module.minecraft.presenter as presenter

from discord.ext import commands
from database.provider.PostgreSQL import postgre
from service.MinecraftService import *

class MinecraftCommand(commands.Cog, name="Minecraft"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='death', help='mc-death [player (use @)] [day_count] [reason] [yyyy-mm-dd (default current date)]')
    async def mc_death(self, ctx, user: discord.User, day: int, reason: str, _time: str= None):
        await update_player_death(str(user.id), day, reason, _time)
        await ctx.send(presenter.get_death_message(user.id))

    @commands.command(name='history', help='see current death stats (last 10 death)')
    async def mc_history(self, ctx):
        try:
            limit = constant.DEATH_HISTORY_ITEM_PER_PAGE
            rows = await get_all_player_dead_history(0, limit)
            totalData = await count_all_player_dead_history()
            totalPage = int(math.ceil(totalData[0]['count'] / limit))
            embed_message = await presenter.get_embed_death_history(self.bot, rows, 1, totalPage)

            res = await ctx.send(embed=embed_message)
            await res.add_reaction('⬅️')
            await res.add_reaction('➡️')

        except Exception as e:
            print("throwing exception")
            print(e)
            # pass
    
    @commands.command(name='history-user', help='mc-history-user [player (use @)]')
    async def mc_history_user(self, ctx, user: discord.User):
        player_name = await self.__get_name_by_id(user.id)
        embed_message = discord.Embed(title=f'{player_name}\'s Death History', description="Death History per Player", color=0x00ff00)

        rows = await get_player_dead_history(user.id, 0)
        message = """
+-------------------+-------------------+-------------------+
|        Days       |       Reason      |       TIME        |
+-------------------+-------------------+-------------------+\n"""
        for row in rows:
            message += f'|{(str(row[0])).center(19)}|{(row[1]).center(19)}|{(str(row[2])).center(19)}|\n'
        message += '+-------------------+-------------------+-------------------+\n'
        embed_message.add_field(name="History", value=f"```{message}```", inline=True)
        await ctx.send(embed=embed_message)

    @commands.command(name='stats', help='see current death stats')
    async def mc_stats(self, ctx):
        embed_message = discord.Embed(title="Minecraft Hardcore Dead Stats", description="Death Counter", color=0x00ff00)
        
        rows = await get_death_stats()
        message = """
+--------------------+--------------------+
|       Player       |        Score       |
+--------------------+--------------------+\n"""
        for row in rows:
            name = await self.__get_name_by_id(row[0])
            message += f'|{name.center(20)}|{(str(row[1])).center(20)}|\n'
        message += '+--------------------+--------------------+\n'
        embed_message.add_field(name="Stats", value=f"```{message}```", inline=True)
        await ctx.send(embed=embed_message)

    @commands.command(name="server", help='Server Information')
    async def mc_server(self, ctx):
        message = await ctx.send('⏳ **Retrieving server info... Please wait...**')
        
        mc_api = os.getenv('MINECRAFT_SERVER_STATS_API')
        mc_server = os.getenv('MINECRAFT_ATERNOS_SERVER')
        url = mc_api + mc_server
        response = requests.get(url)
        if response.status_code != 200:
            await message.edit(content='**🛑 Server is stopped**')
            return
    
        embed_message = self.__get_embed_server_status(response.json())
        await message.edit(content=None, embed=embed_message)

    @commands.command(name='coord', help='see/save coordinates [x] [y] [z] [description]')
    async def mc_coord(self, ctx, x:int = 300, y:int = 300, z:int = 300, *description:str):
        #coordinate minecraft mentok di 255
        if len(description) == 0 and x == 300 and y == 300 and z == 300:
            try:
                rows = await get_all_coordinates(0)
                embed_message = await self.__get_embed_saved_coordinates(rows)

                res = await ctx.send(embed=embed_message)
                await res.add_reaction('⬅️')
                await res.add_reaction('➡️')
                return
            except Exception as e:
                print(e)

        await insert_landmark(' '.join(description), x, y, z)
        await ctx.send(f'**💾 Coordinate for `{" ".join(description)}` at `x: {x} y: {y} z: {z}` is saved**')

    async def __get_name_by_id(self, id):
        user = await self.bot.fetch_user(id)
        return user.name
    
    def __get_embed_server_status(self, info):
        embed_message = discord.Embed(title='Wolvmc Aternos Server', 
                                        description=f"Server Status for {info['hostname']}", 
                                        color=0x00ff00)

        is_online = 'Online' if info['online'] else 'Offline'
        embed_message.add_field(name='Status', value=f'{is_online}', inline=True)
        if info['online']:
            embed_message.add_field(name='State', value=f'{info["version"]}', inline=True)
            embed_message.add_field(name='IP', value=f'{info["ip"]}:{info["port"]}', inline=False)

            player_online = info['players']['online']
            player_max = info['players']['max']
            embed_message.add_field(name='Online Players', value=f'{player_online}/{player_max}', inline=False)
        
        return embed_message
        
