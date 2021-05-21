from discord.ext.commands import Bot
from module.minecraft.command import MinecraftCommand
from module.minecraft.event import MinecraftEvent

def register_minecraft_cog(bot: Bot):
    try:
        bot.add_cog(MinecraftCommand(bot))
        bot.add_cog(MinecraftEvent(bot))
    except Exception as e:
        print(e)