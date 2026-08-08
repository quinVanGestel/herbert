import random
import discord
import json
from discord.ext import commands

with open('botConfig.json', 'r') as file:
    botConfig = json.load(file)

equippableRoles:list[str] = botConfig['equippableRoles']
humanGreetings:list[str] = botConfig['humanGreetings']
botGreetings:list[str] = botConfig['botGreetings']
botPunctuations:list[str] = botConfig['botPunctuations']

async def DigestMessage(message: discord.Message) -> None:
    if humanGreetings.__contains__(message.content.lower()):
        await Greet(message.channel)

async def Greet(channel: discord.channel) -> None:
    await channel.send(random.choice(botGreetings)+random.choice(botPunctuations))
    
async def DisableBot(bot: commands.Bot) -> None:
    await bot.close()
