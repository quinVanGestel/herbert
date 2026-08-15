import random
import discord
from discord.ext import commands
import settings


async def DigestMessage(message: discord.Message) -> None:
    if settings.humanGreetings.__contains__(message.content.lower()):
        await Greet(message.channel)

async def Greet(channel: discord.channel) -> None:
    await channel.send(random.choice(settings.botGreetings)+random.choice(settings.botPunctuations))
    
async def DisableBot(bot: commands.Bot) -> None:
    await bot.close()
    
    # deffo wrote this myself and didn't steal it
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]