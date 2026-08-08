import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import json
import asyncio
from cogs import roles


load_dotenv()

#region Import Config
with open('botConfig.json', 'r') as file:
    botConfig = json.load(file)

equippableRoles:list[str] = botConfig['equippableRoles']
humanGreetings:list[str] = botConfig['humanGreetings']
botGreetings:list[str] = botConfig['botGreetings']
botPunctuations:list[str] = botConfig['botPunctuations']
#endregion

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
        print("Cogs loaded (hopefully)")
        
        print("Starting bot...")
        await bot.start(TOKEN)
        print("Bot started! (hopefully)")

async def LoadCogs() -> None:
    await bot.add_cog(roles.Roles(bot, equippableRoles))
    

asyncio.run(Main())


# |
# v things I haven't moved to a misc cog yet
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready! :3')
    for guild in bot.guilds:
        await Greet(guild.system_channel)

@bot.event
async def on_message(message: discord.Message):
    print(f'{message.author} whose ID is {message.author.id} sent {message.content}')
    
    if (bot.user == None):
        print("Herbert's account is None... Huh?")
        return
    if (message.author.id == bot.user.id):
        print("Herbert sent this message. Herbert refuses to talk to himself.")
        return
    
    await DigestMessage(message)
    
    await bot.process_commands(message)

async def DigestMessage(message: discord.Message):
    if humanGreetings.__contains__(message.content.lower()):
        await Greet(message.channel)

async def Greet(channel: discord.channel):
    await channel.send(random.choice(botGreetings)+random.choice(botPunctuations))

@bot.command()
async def meow(ctx: commands.Context):
    await ctx.send("mrrrp :3")


        
@bot.command()
@commands.has_guild_permissions(administrator=True)
async def shutdown(ctx:commands.Context):
    await ctx.send("Father... why....")
    await bot.close()
@shutdown.error
async def shutdown_error(ctx:commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("I refuse. You're not my real dad!")
