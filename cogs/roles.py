import discord
from discord.ext import commands
import settings
import helper

class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def equip(self, ctx: commands.Context,*, args: str):
        print(f"equip was called with arguments {args}")
        seperatedArgs: tuple = await ExtractMembersFromString(ctx, args)
        # print(f"seperatedargs tuple item one: {seperatedArgs[0]} \nseperatedargs tuple item two: {seperatedArgs[1]}")
        roleName = seperatedArgs[0]
        recipients: list[discord.Member] = seperatedArgs[1]
        if len(recipients) == 0:
            roleName=args
            recipients.append(ctx.author)
        print(roleName)
        print(recipients)

        role = discord.utils.get(ctx.guild.roles, name=roleName)

        for recipient in recipients:
            print(f"{ctx.author.display_name} requested to equip {roleName} for {recipient.display_name}")
            
            if not await AssignRoleIsPossible(ctx, role, recipient, True):
                return
            
            if not await AssignRoleIsAllowed(ctx, role, recipient, True):
                return
            
            await recipient.add_roles(role)
            await ctx.send(f"Gave {roleName} to {recipient.display_name}")
            print(f"Gave {roleName} to {recipient.display_name}")

    @commands.command()
    async def unequip(self, ctx: commands.Context,*, roleName: str):
        # if recipient is None:
        recipient = ctx.author
        
        print(f"{ctx.author.display_name} requested to unequip {roleName} for {recipient.display_name}")

        role = discord.utils.get(ctx.guild.roles, name=roleName)

        if not await AssignRoleIsPossible(ctx, role, recipient, False):
            return
        
        if not await AssignRoleIsAllowed(ctx, role, recipient, False):
            return
    
        await recipient.remove_roles(role)
        await ctx.send(f"Removed {roleName} from {recipient.display_name}")
        print(f"Removed {roleName} from {recipient.display_name}")

async def ExtractMembersFromString(ctx: commands.Context, string: str) -> tuple:
    print(f"ExtractMemberFromString called with argument {string}")
    splitString: list[str] = string.split()
    members: list[discord.Member] = []
    
    print("Running through mentions")
    for mention in ctx.message.mentions:
        print(f"Checking {mention.display_name}")
        if isinstance(mention, discord.Member):
            members.append(mention)
            print(f"Added {mention.display_name}")
            print(f"pre: {splitString}")
            splitString: list[str] = helper.remove_values_from_list(splitString, f"<@{mention.id}>")
            print(f"post: {splitString}")
    
    print("Running through any int strings that may be in splitString")
    for word in splitString:
        try:
            wordIntified: int = int(word)
        except:
            print("Split string item cannot be cast to int")
        else:
            print(f"Intified {word}")
            try:
                member: discord.Member = await ctx.guild.fetch_member(int(wordIntified))
            except:
                print("Fetching member with splitStringItemIntified made crash :(")
            else:
                if member is not None:
                    members.append(member)
                    splitString.remove(word)
                    print(f"Successfully added {member.display_name} and removed {word} from splitString.")
                    
    filteredString:str = ""
    filteredString = " ".join(splitString)
    print(f"Final result: {filteredString}")
    return (filteredString, members)
    

async def AssignRoleIsPossible(ctx: commands.Context, role: discord.Role, recipient: discord.Member, equip: bool,discordMessageOnFailure: bool = True, debugLogOnFailure: bool = True) -> bool :
    print("Checking if assignroleispossible")
    if role is None:
        if (discordMessageOnFailure):
            await ctx.send("Role not found.")
        if (debugLogOnFailure):
            await print("Role not found.")
        return False

    if not role.is_assignable():
        if (discordMessageOnFailure):
            await ctx.send(f"I lack the permissions required to assign {role.name}")
        if (debugLogOnFailure):
            await print(f"I lack the permissions required to assign {role.name}")
        return False
    
    if equip:
        if await UserHasRole(recipient.roles, role.name):
            if (discordMessageOnFailure):
                await ctx.send(f"{recipient.display_name} already has {role.name}, silly goose.")
            if (debugLogOnFailure):
                await print(f"{recipient.display_name} already has {role.name}, silly goose.")
            return False
    else:
        if not await UserHasRole(recipient.roles, role.name):
            if (discordMessageOnFailure):
                await ctx.send(f"{recipient.display_name} doesn't have {role.name}, silly goose.")
            if (debugLogOnFailure):
                await print(f"{recipient.display_name} doesn't have {role.name}, silly goose.")
            return False
            
    return True

async def AssignRoleIsAllowed(ctx: commands.Context, role: discord.Role, recipient: discord.Member,equip: bool, discordMessageOnFailure: bool = True, debugLogOnFailure: bool = True) -> bool:
    print("Checking if AssignRoleIsAllowed")
    if not settings.equippableRoles.__contains__(role.name):
        if (discordMessageOnFailure):
            await ctx.send("This role isn't assignable.")
        if (debugLogOnFailure):
            await print("This role isn't assignable.")
        return False
    
    if recipient.id is not ctx.author.id and not ctx.author.guild_permissions.manage_roles:
        if (discordMessageOnFailure):
            await ctx.send("You do not have manage roles permissions.")
        if (debugLogOnFailure):
            await print("You do not have manage roles permissions.")
        return False
    return True

async def UserHasRole(equippedRoles: list[discord.Role], roleName: str) -> bool:
    for equippedRole in equippedRoles:
        if roleName == equippedRole.name:
            print(roleName)
            return True
    return False
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
    