import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN: str = str(os.getenv('DISCORD_TOKEN'))


humanGreetings = ["hi", "hello","hi herbert"]
botGreetings = ["hiii", "greetings", "hello there"]
botPunctuations = [":3", "!"]

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=':3', intents=intents)




@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready! :3')

@bot.event
async def on_message(message: discord.Message):
    print(f'{message.author} whose ID is {message.author.id} sent {message.content}')
    
    if (bot.user == None):
        print("Herbert's account is None... Huh?")
        return
    if (message.author.id == bot.user.id):
        print("Herbert sent this message. Herbert refuses to talk to himself.")
        return
    await message.channel.send(botGreetings[0])

@commands.has_guild_permissions(administrator=True)
async def shutdown():
    exit()

bot.run(token=TOKEN, log_handler=handler,log_level=logging.DEBUG)