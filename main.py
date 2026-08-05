import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import json

load_dotenv()

TOKEN: str = str(os.getenv('DISCORD_TOKEN'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#region Config
with open('botConfig.json', 'r') as file:
    botConfig = json.load(file)

print(botConfig)

for item in botConfig:
    print(item)

commandPrefix:str = botConfig['commandPrefix']
equippableRoles:list[str] = botConfig['equippableRoles']
humanGreetings:list[str] = botConfig['humanGreetings']
botGreetings:list[str] = botConfig['botGreetings']
botPunctuations:list[str] = botConfig['botPunctuations']
#endregion

bot = commands.Bot(command_prefix=commandPrefix, intents=intents)

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
async def equip(ctx: commands.Context, roleName: str):
    print(f"User requested to equip {roleName}")
    
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    if role is None:
        print("Role not found")
        await ctx.send("Role not found.")
        return
    
    for equippedRole in ctx.author.roles:
        if roleName == equippedRole.name:
            await ctx.send(f"You already have {roleName} silly goose.")
            return
        
    if not equippableRoles.__contains__(roleName):
        await ctx.send("This role is not equippable.")
        return
    
    await ctx.author.add_roles(role)
    await ctx.send(f"Gave {roleName} to {ctx.author.display_name}")
    print(f"Gave {roleName} to {ctx.author.display_name}")
    
@bot.command()
async def unequip(ctx: commands.Context, roleName: str):
    print(f"User requested to unequip {roleName}")
    
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    if role is None:
        print("Role not found")
        await ctx.send("Role not found.")
        return
    
    userHasRole:bool = False
    for equippedRole in ctx.author.roles:
        if roleName == equippedRole.name:
            userHasRole = True
    if not userHasRole:
        await ctx.send(f"You don't have {roleName} silly goose.")
        return
    
    if not equippableRoles.__contains__(roleName):
        await ctx.send("This role is not unequippable.")
        return
    
    await ctx.author.remove_roles(role)
    await ctx.send(f"Removed {roleName} from {ctx.author.display_name}")
    print(f"Removed {roleName} from {ctx.author.display_name}")
    return
        
@bot.command()
@commands.has_guild_permissions(administrator=True)
async def shutdown(ctx:commands.Context):
    await ctx.send("Father... why....")
    await bot.close()
@shutdown.error
async def shutdown_error(ctx:commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("I refuse. You're not my real dad!")

bot.run(token=TOKEN, log_handler=handler,log_level=logging.DEBUG)