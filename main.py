import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random


load_dotenv()

TOKEN: str = str(os.getenv('DISCORD_TOKEN'))

equippableRoles = ["purple","red"]

humanGreetings = ["hi", "hello","hi herbert"]
botGreetings = ["hiii", "greetings", "hello there"]
botPunctuations = [" :3", "!",".","..."," :D"]

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='herb ', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready! :3')
    for guild in bot.guilds:
        await guild.system_channel.send(random.choice(botGreetings)+random.choice(botPunctuations))

@bot.event
async def on_message(message: discord.Message):
    print(f'{message.author} whose ID is {message.author.id} sent {message.content}')
    
    if (bot.user == None):
        print("Herbert's account is None... Huh?")
        return
    if (message.author.id == bot.user.id):
        print("Herbert sent this message. Herbert refuses to talk to himself.")
        return
    
    await bot.process_commands(message)

@bot.command()
async def meow(ctx: commands.Context):
    await ctx.send("mrrrp :3")

@bot.command()
async def equip(ctx: commands.Context, roleName: str):
    print(f"User requested to equip {roleName}")
    
    for equippedRole in ctx.author.roles:
        if roleName == equippedRole.name:
            await ctx.send(f"You already have {roleName} silly goose.")
            return
    
    if not equippableRoles.__contains__(roleName):
        await ctx.send("This role is not equippable.")
        return
    
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    if role is None:
        print("Role not found")
        await ctx.send("Role not found.")
        return
    
    await ctx.author.add_roles(role)
    await ctx.send(f"Gave {roleName} to {ctx.author.display_name}")
    print(f"Gave {roleName} to {ctx.author.display_name}")
    
@bot.command()
async def unequip(ctx: commands.Context, roleName: str):
    print(f"User requested to unequip {roleName}")
    
    for equippedRole in ctx.author.roles:
        if roleName == equippedRole.name:
            await ctx.send(f"You don't have {roleName} silly goose.")
            return
        
    if not equippableRoles.__contains__(roleName):
        await ctx.send("This role is not unequippable.")
        return
    
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    if role is None:
        print("Role not found")
        await ctx.send("Role not found.")
        return
    
    await ctx.author.remove_roles(role)
    await ctx.send(f"Removed {roleName} from {ctx.author.display_name}")
    print(f"Removed {roleName} from {ctx.author.display_name}")

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def shutdown(ctx:commands.Context):
    await ctx.send("Father... why....")
    await bot.close()
@shutdown.error
async def shutdown_error(ctx):
    await ctx.send("I refuse. You're not my real dad!")

bot.run(token=TOKEN, log_handler=handler,log_level=logging.DEBUG)