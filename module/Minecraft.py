import discord

from discord.ext import commands
from database.provider.PostgreSQL import postgre
from service.MinecraftService import *

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DEATH_HISTORY_TITLE = "Minecraft Hardcore Death History"
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        embed = reaction.message.embeds[0]
        if(embed.title == self.DEATH_HISTORY_TITLE):
            # kasih validasi kalo yang boleh next cuma yang nge request
            page = int(embed.footer.text)
            offset = 0
            limit = 10
            if(reaction.emoji == '➡️'):
                offset = page * limit
                page+=1

            elif(reaction.emoji == '⬅️' and page > 1 ):
                page-=1
                offset = (page-1) * limit

            rows = await get_all_player_dead_history(offset, limit)
            if len(rows) > 0:
                embed_message = await self.__get_embed_death_history(rows, page)
                await reaction.message.edit(embed=embed_message)
            return

    # TODO: delete after all name is migrated
    @commands.command(name='mc-rename', help='mc-rename [current player name stored] [player\'s discord (use @)]')
    async def mc_rename(self, ctx, name: str, user: discord.User):
        await rename_player(name, str(user.id))
        await ctx.send(f'{name} is now updated to <@{user.id}>')
        
    @commands.command(name='mc-death', help='mc-death [player (use @)] [day_count] [reason] [yyyy-mm-dd (default current date)]')
    async def mc_death(self, ctx, user: discord.User, day: int, reason: str, _time: str= None):
        await update_player_death(str(user.id), day, reason, _time)
        await ctx.send(f"<@{user.id}> Lol ⬆️⬆️" if user.id == 289434773972058113 else 'Stats Updated')

    @commands.command(name='mc-history', help='see current death stats (last 10 death)')
    async def mc_history(self, ctx):
        try:
            rows = await get_all_player_dead_history(0)
            embed_message = await self.__get_embed_death_history(rows)

            res = await ctx.send(embed=embed_message)
            await res.add_reaction('⬅️')
            await res.add_reaction('➡️')

        except Exception as e:
            print(e)
    
    @commands.command(name='mc-history-user', help='mc-history-user [player (use @)]')
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

    @commands.command(name='mc-stats', help='see current death stats')
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

    @commands.command(name="mc-server", help='Server Information')
    async def mc_server(ctx, *message):
        message = await ctx.send('Retrieving server info... Please wait...')
        
        mc_api = os.getenv('MINECRAFT_SERVER_STATS_API')
        mc_server = os.getenv('MINECRAFT_ATERNOS_SERVER')
        url = mc_api + mc_server
        response = requests.get(url)
        if response.status_code != 200:
            await message.edit(content='Server is stopped')
            return
    
        embed_message = get_embed_server_status(response.json())
        await message.edit(content=None, embed=embed_message)

    async def __get_embed_death_history(self, rows:list, page:int = 1):
        embed_message = discord.Embed(
            title=self.DEATH_HISTORY_TITLE, 
            description="Death history sorted from latest death", 
            color=0x00ff00
        )

        message = """
+--------------+--------------+--------------+--------------+
|    Player    |     Days     |    Reason    |    TIME      |
+--------------+--------------+--------------+--------------+\n"""
        for row in rows:
            name = await self.__get_name_by_id(row[1])
            message += f'|{name.center(14)}|{(str(row[2])).center(14)}|{row[3].center(14)}|{str(row[4]).center(14)}|\n'
        message += '+--------------+--------------+--------------+--------------+\n'

        embed_message.add_field(name="History", value=f"```{message}```", inline=True)
        embed_message.set_footer(text=str(page))
        return embed_message

    async def __get_name_by_id(self, id):
        user = await self.bot.fetch_user(id)
        return user.name
    
    def get_embed_server_status(info):
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
        
def setup(bot):
    bot.add_cog(Minecraft(bot))
