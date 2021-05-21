import discord
import textwrap
import module.minecraft.constant as constant
import module.helper as helper


def get_death_message(userId: int):
    return f"<@{userId}> Lol ⬆️⬆️" if userId == 289434773972058113 else f"**😈 and <@{userId}> goes straight to the hell**"


async def get_embed_death_history(bot, rows:list, page:int, totalPage:int):
    embed_message = discord.Embed(
        title=constant.DEATH_HISTORY_TITLE, 
        description="Death history sorted from latest death", 
        color=0x00ff00
    )

    message = textwrap.dedent(
        """
        +--------------+--------------+--------------+--------------+
        |    Player    |     Days     |    Reason    |    TIME      |
        +--------------+--------------+--------------+--------------+\n"""
    )
    for row in rows:
        name = await helper.get_name_by_discord_id(bot, row['player'])
        message += f'|{name.center(14)}|{(str(row["days"])).center(14)}|{row["reason"].center(14)}|{str(row["time"]).center(14)}|\n'
    message += '+--------------+--------------+--------------+--------------+\n'
    print(message)

    embed_message.add_field(name="History", value=f"```{message}```", inline=True)
    embed_message.set_footer(text=f'Page: {page}/{totalPage}')
    return embed_message


async def get_embed_saved_coordinates(rows:list, page:int, totalPage:int):
    embed_message = discord.Embed(
        title=constant.SAVED_COORDINATES_TITLE, 
        description="Minecraft saved coordinates for landmarks and others", 
        color=0x00ff00
    )
    message = textwrap.dedent("""
        +--------------------+-------+-------+-------+
        |     Description    |   X   |   Y   |   Z   |
        +--------------------+-------+-------+-------+\n""")
    for row in rows:
        message += f'|{(str(row[1])).center(20)}|{(str(row[2])).center(7)}|{(str(row[3])).center(7)}|{str(row[4]).center(7)}|\n'
    message += '+--------------------+-------+-------+-------+\n'

    embed_message.add_field(name="Coordinates", value=f"```{message}```", inline=True)
    embed_message.set_footer(text=f'Page: {page}/{totalPage}')
    return embed_message

