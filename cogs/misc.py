import discord
from discord.ext import commands
import helper
import settings

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def meow(self, ctx: commands.Context):
        await ctx.send("mrrrp :3")        
        
    @commands.command()
    async def shutdown(self, ctx:commands.Context):
        if ctx.author.id != settings.OWNERID:
            await ctx.send("I refuse. You're not my real dad!")
            return
    
        await ctx.send("Father... why....")
        await helper.DisableBot(self.bot)

            
async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))