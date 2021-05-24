import config
import discord
import time
import yagmail

from discord.ext import commands
from app.database.provider.PostgreSQL import postgre
from app.discord.module.minecraft import register_minecraft_cog
from app.service.Log import Log

discord_bot = commands.Bot(command_prefix='!mc-')

@discord_bot.event
async def on_ready():
    await postgre.connect()
    
    # Register module
    register_minecraft_cog(discord_bot)

    print(f'{discord_bot.user.name} has connected to discord')
    await discord_bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Someone Dying"))


@discord_bot.event
async def on_command_error(ctx, error):
    Logger = Log()
    err = f'Unhandled Exception: {error}'
    await Logger.error(err)

    await ctx.send('☹️ Ooops something happened! Please contact your admin')
    __send_error_to_email(err)


def __send_error_to_email(err):
    # kirim email nya ga async, jadi agak nunggu gitu
    # makanya buat skrg send email nya setelah nulis di err.log dan chat discord biar ga nunggu

    if (config.DEBUG_EMAIL == ""):
        return
    
    email_content = f"[{time.asctime()}]\n{err}\n"
    yag = yagmail.SMTP(config.DEBUG_EMAIL, config.DEBUG_EMAIL_PASSWORD)
    contents = [
        email_content
    ]
    yag.send(config.DEBUG_EMAIL, 'Minecraft Error', contents) 