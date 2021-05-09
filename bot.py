from imports import *
from database.provider.PostgreSQL import postgre
from database.migrations import migrate_db

load_dotenv()

# Modules
modules = [
    "module.Minecraft"
]

#TIMER
start_time = time.time()
buffer_time = 10 * 60 # 15 minutes
exit_after = 24 * 60 * 60 # 24 hours in second

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await postgre.connect()
    await migrate_db()

    for m in modules:
        bot.load_extension(m)

    print(f'{bot.user.name} has connected to discord')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Someone Dying"))

@bot.event
async def on_command_error(ctx, error):
    with open('err.log', 'a') as f:
        f.write(f'Unhandled Exception: {error}\n')
    await ctx.send('Ooops something happened! Please contact your admin :(')


#Start bot
def connectBot(TOKEN_DISCORD):
    bot.run(TOKEN_DISCORD)

if __name__ == '__main__':
    #Bot Credential
    TOKEN = os.getenv('DISCORD_TOKEN') 
    p = multiprocessing.Process(target=connectBot, name="connectBot", args=(TOKEN,))
    p.start()

    #Timer
    while(time.time() - start_time <= (exit_after - buffer_time)):
        time.sleep(10 * 60) #sleep every 10 mins

    #Exit program after timer end
    p.terminate()
    p.join()
    sys.exit()

