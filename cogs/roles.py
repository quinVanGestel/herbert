import discord
from discord.ext import commands
import settings

class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None # no clue what this does but the tutorial said to add it so ig I'll add it

    @commands.command()
    async def equip(self, ctx: commands.Context, roleName: str,recipient: discord.Member = None):
        if recipient is None:
            recipient = ctx.author
        
        print(f"{recipient.display_name} requested to equip {roleName}")
        
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.send("Role not found.")
            return

        if UserHasRole(recipient.roles, roleName):
            await ctx.send(f"{recipient.display_name} already has {roleName} silly goose.")
            return
        
        if not settings.equippableRoles.__contains__(roleName):
            await ctx.send("This role is not equippable.")
            return
        
        await recipient.add_roles(role)
        await ctx.send(f"Gave {roleName} to {recipient.display_name}")
        print(f"Gave {roleName} to {recipient.display_name}")
    
    @commands.command()
    async def unequip(self, ctx: commands.Context, roleName: str, recipient: discord.Member = None):
        if recipient is None:
            recipient = ctx.author
        
        print(f"{recipient.display_name} requested to unequip {roleName}")

        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.send("Role not found.")
            return

        if not UserHasRole(recipient.roles, roleName):
            await ctx.send(f"{recipient.display_name} doesn't have {roleName} silly goose.")
            return
        
        if not settings.equippableRoles.__contains__(roleName):
            await ctx.send("This role is not unequippable.")
            return
        
        await recipient.remove_roles(role)
        await ctx.send(f"Removed {roleName} from {recipient.display_name}")
        print(f"Removed {roleName} from {recipient.display_name}")
        
    
def UserHasRole(equippedRoles: list[discord.Role], roleName: str) -> bool:
    for equippedRole in equippedRoles:
        if roleName == equippedRole.name:
            print(roleName)
            return True
    return False
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
    