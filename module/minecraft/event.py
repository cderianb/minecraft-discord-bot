import re
import module.minecraft.constant as constant
import module.minecraft.presenter as presenter
import service.MinecraftService as service

from discord.ext import commands

class MinecraftEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if len(reaction.message.embeds) <= 0:
            return
        
        embed = reaction.message.embeds[0]
        values = re.findall(r'\d+', embed.footer.text)
        currentPage, totalPage = int(values[0]), int(values[1])
        title = embed.title
        action = None

        if(reaction.emoji == '➡️' and currentPage < totalPage):
            action = constant.NEXT
        elif(reaction.emoji == '⬅️' and currentPage > 1):
            action = constant.PREV
        else:
            return

        content = None
        if title == constant.DEATH_HISTORY_TITLE:
            content = await self.__update_dead_history_page(currentPage, totalPage, action)
        elif title == constant.SAVED_COORDINATES_TITLE:
            content = await self.__update_saved_coordinates_page(currentPage, totalPage, action)

        if (content != None):
            await reaction.message.edit(embed = content)
    

    def __update_pagination_property(self, page: int, limit: int, action: int):
        if action == constant.NEXT:
            offset = page * limit
            return [page+1, offset]
        
        elif action == constant.PREV:
            page = page - 1
            offset = (page-1) * limit
            return [page, offset]


    async def __update_dead_history_page(self, currentPage: int, totalPage: int, action: int):
        limit = constant.DEATH_HISTORY_ITEM_PER_PAGE
        page, offset = self.__update_pagination_property(currentPage, limit, action)
        rows = await service.get_all_player_dead_history(offset, limit)
        return await presenter.get_embed_death_history(self.bot, rows, page, totalPage)


    async def __update_saved_coordinates_page(self, currentPage: int, totalPage: int, action: int):
        limit = constant.COORDINATES_ITEM_PER_PAGE
        page, offset = self.__update_pagination_property(currentPage, limit, action)
        rows = await service.get_all_coordinates(offset, limit)
        return await presenter.get_embed_saved_coordinates(rows, page, totalPage)
