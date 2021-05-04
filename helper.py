from imports import *

# rows : data shown in table
def get_embed_death_history(db, rows:list, page:int = 1):
    embed_message = discord.Embed(title=DEATH_HISTORY_TITLE, 
                                    description="Death history sorted from latest death", 
                                    color=0x00ff00)

    message = """
+--------------+--------------+--------------+--------------+
|    Player    |     Days     |    Reason    |    TIME      |
+--------------+--------------+--------------+--------------+\n"""
    for row in rows:
        message += f'|{row[1].center(14)}|{(str(row[2])).center(14)}|{row[3].center(14)}|{str(row[4]).center(14)}|\n'
    message += '+--------------+--------------+--------------+--------------+\n'

    embed_message.add_field(name="History", value=f"```{message}```", inline=True)
    embed_message.set_footer(text=str(page))
    return embed_message