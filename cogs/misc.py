import discord
from discord.ext import commands
import helper

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None # no clue what this does but the tutorial said to add it so ig I'll add it
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is ready! :3')
        for guild in self.bot.guilds:
            await helper.Greet(guild.system_channel)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f'{message.author} whose ID is {message.author.id} sent {message.content}')
        
        if (self.bot.user == None):
            print("Herbert's account is None... Huh?")
            return
        if (message.author.id == self.bot.user.id):
            print("Herbert sent this message. Herbert refuses to talk to himself.")
            return
        
        await helper.DigestMessage(message)
        
        await self.bot.process_commands(message)


    @commands.command()
    async def meow(self, ctx: commands.Context):
        await ctx.send("mrrrp :3")
        
        
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def shutdown(self, ctx:commands.Context):
        await ctx.send("Father... why....")
        await helper.DisableBot(self.bot)
    @shutdown.error
    async def shutdown_error(ctx:commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I refuse. You're not my real dad!")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))