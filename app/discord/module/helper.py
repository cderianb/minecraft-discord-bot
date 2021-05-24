import asyncio

from discord.ext.commands import Bot

cachedName = {}

async def get_name_by_discord_id(bot: Bot, id: int):
    if (id not in cachedName):
        user = await bot.fetch_user(id)
        cachedName[id] = user.name
    
    return cachedName[id]


async def add_pagination_arrow_reaction(res):
    await asyncio.gather(
        res.add_reaction('⬅️'),
        res.add_reaction('➡️')
    )
