from discord.ext.commands import Bot
from app.discord.module.minecraft.command import MinecraftCommand
from app.discord.module.minecraft.event import MinecraftEvent

def register_minecraft_cog(bot: Bot):
    try:
        bot.add_cog(MinecraftCommand(bot))
        bot.add_cog(MinecraftEvent(bot))
    except Exception as e:
        print(e)