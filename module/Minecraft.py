import discord

from discord.ext import commands
from database.provider.PostgreSQL import postgre

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = postgre.get()
        self.DEATH_HISTORY_TITLE = "Minecraft Hardcore Death History"
        
    @commands.command(name='mc-death', help='mc-death [player (use @)] [day_count] [reason] [yyyy-mm-dd (default current date)]')
    async def mc_death(self, ctx, user: discord.User, day: int, reason: str, _time: str= None):
        time = _time if _time != None else "NOW()"
        connection = await self.db.acquire()
        async with connection.transaction():
            query = f'INSERT INTO dead(player, days, reason, time) VALUES($1, $2, $3, {time});'
            await self.db.execute(query, str(user.id), day, reason)
        await self.db.release(connection)

        # TODO: insult more!!
        await ctx.send(f"<@{user.id}> Lol ⬆️⬆️" if user.id == '289434773972058113' else 'Stats Updated')

    @commands.command(name='mc-history', help='see current death stats (last 10 death)')
    async def mc_history(self, ctx):
        try:
            query = "SELECT * FROM dead ORDER BY id DESC LIMIT 10;"
            rows = await self.db.fetch(query)
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

        query = f"SELECT days, reason, time FROM dead WHERE player = '{user.id}' ORDER BY id DESC LIMIT 10;"
        rows = await self.db.fetch(query) # return list of all row
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
        
        query = "select player, count(*) from dead group by player ORDER BY 2 DESC, 1 LIMIT 10;"
        rows = await self.db.fetch(query)
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

def setup(bot):
    bot.add_cog(Minecraft(bot))