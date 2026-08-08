import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

#region Bot initialisation
TOKEN: str = str(os.getenv('DISCORD_TOKEN'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

commandPrefix:str = "herb"

bot = commands.Bot(command_prefix=commandPrefix, intents=intents)
bot.owner_id = 1135499866387259544
bot.strip_after_prefix = True
#endregion

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
    print("Cogs loaded")
    
asyncio.run(Main())