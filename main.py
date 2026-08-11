import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import settings
import helper

load_dotenv()

#region Bot initialisation
TOKEN: str = str(os.getenv('DISCORD_TOKEN'))

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=settings.commandPrefix, 
    intents=intents, 
    owner_id=settings.OWNERID, 
    strip_after_prefix=settings.stripAfterPrefix
    )
#endregion

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready! :3')
    for guild in bot.guilds:
        await helper.Greet(guild.system_channel)

@bot.event
async def on_message(message: discord.Message):
    if (message.author.id == bot.user.id):
        print("Herbert sent this message. Herbert refuses to listen to himself.")
        return
    
    print(f'{message.author} whose ID is {message.author.id} sent {message.content}')
    
    await helper.DigestMessage(message)
    
    message.content = message.content.lower()
    await bot.process_commands(message)

async def Main() -> None:
    async with bot:
        print("Loading cogs...")
        await LoadCogs()
        
        print("Starting bot...")
        await bot.start(TOKEN)
        print("Failed to run bot.start.")

async def LoadCogs() -> None:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")
    print("Cogs loaded")
    
asyncio.run(Main())