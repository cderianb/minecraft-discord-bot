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
    err = f'[{time.asctime()}]\nUnhandled Exception: {error}\n'
    
    with open('err.log', 'a') as f:
        f.write(err)

    await ctx.send('☹️ Ooops something happened! Please contact your admin')

    #kirim email nya ga async, jadi agak nunggu gitu
    #makanya buat skrg send email nya setelah nulis di err.log dan chat discord biar ga nunggu
    email = os.getenv('KEHUJANAN_EMAIL')
    password = os.getenv('KEHUJANAN_PASSWORD')
    yag = yagmail.SMTP(email, password)
    contents = [
            err
        ]
    yag.send(email, 'Minecraft Error', contents) 
    


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

