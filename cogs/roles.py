import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot, equippableRoles: list[str]):
        self.bot = bot
        self._last_member = None # no clue what this does but the tutorial said to add it so ig I'll add it
        self.equippableRoles = equippableRoles
    
    @commands.command()
    async def equip(self, ctx: commands.Context, roleName: str):
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
        
        if not self.equippableRoles.__contains__(roleName):
            await ctx.send("This role is not equippable.")
            return
    
        await ctx.author.add_roles(role)
        await ctx.send(f"Gave {roleName} to {ctx.author.display_name}")
        print(f"Gave {roleName} to {ctx.author.display_name}")
    
    @commands.command()
    async def unequip(self, ctx: commands.Context, roleName: str):
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
        
        if not self.equippableRoles.__contains__(roleName):
            await ctx.send("This role is not unequippable.")
            return
        
        await ctx.author.remove_roles(role)
        await ctx.send(f"Removed {roleName} from {ctx.author.display_name}")
        print(f"Removed {roleName} from {ctx.author.display_name}")
        return