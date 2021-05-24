import discord
import math
import os
import requests
import app.discord.module.minecraft.constant as constant
import app.discord.module.helper as helper
import app.discord.module.minecraft.presenter as presenter
import app.service.MinecraftService as service

from discord.ext import commands

class MinecraftCommand(commands.Cog, name="Minecraft"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='death', help='mc-death [player (use @)] [day_count] [reason] [yyyy-mm-dd (default current date)]')
    async def mc_death(self, ctx, user: discord.User, day: int, reason: str, _time: str= None):
        await service.update_player_death(str(user.id), day, reason, _time)
        await ctx.send(presenter.get_death_message(user.id))

  
    @commands.command(name='history', help='see current death stats (last 10 death)')
    async def mc_history(self, ctx):
        try:
            limit = constant.DEATH_HISTORY_ITEM_PER_PAGE
            rows = await service.get_all_player_dead_history(0, limit)
            totalData = await service.count_all_player_dead_history()
            totalPage = int(math.ceil(totalData[0]['count'] / limit))
            embed_message = await presenter.get_embed_death_history(self.bot, rows, 1, totalPage)

            res = await ctx.send(embed=embed_message)
            await helper.add_pagination_arrow_reaction(res)

        except Exception as e:
            pass
    

    @commands.command(name='history-user', help='mc-history-user [player (use @)]')
    async def mc_history_user(self, ctx, user: discord.User):
        player_name = await helper.get_name_by_discord_id(self.bot, user.id)
        rows = await service.get_player_dead_history(user.id, 0)

        embed_message = presenter.get_user_death_history_message(player_name, rows)
        await ctx.send(embed=embed_message)


    @commands.command(name='stats', help='see current death stats')
    async def mc_stats(self, ctx):
        rows = await service.get_death_stats()
        embed_message = await presenter.get_death_stats_message(self.bot, rows)
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
    
        embed_message = presenter.get_embed_server_status(response.json())
        await message.edit(content=None, embed=embed_message)


    @commands.command(name='coord', help='see/save coordinates [x] [y] [z] [description]')
    async def mc_coord(self, ctx, x:int = 300, y:int = 300, z:int = 300, *description:str):
        #coordinate minecraft mentok di 255
        if len(description) == 0 and x == 300 and y == 300 and z == 300:
            try:
                limit = constant.COORDINATES_ITEM_PER_PAGE
                rows = await service.get_all_coordinates(0, limit)
                totalData = await service.count_coordinates()
                totalPage = int(math.ceil(totalData[0]['count'] / limit))
                embed_message = await presenter.get_embed_saved_coordinates(rows, 1, totalPage)

                res = await ctx.send(embed=embed_message)
                await helper.add_pagination_arrow_reaction(res)

            except Exception as e:
                print(e)
                
            finally:
                return

        await service.insert_landmark(' '.join(description), x, y, z)
        await ctx.send(f'**💾 Coordinate for `{" ".join(description)}` at `x: {x} y: {y} z: {z}` is saved**')
    
        
