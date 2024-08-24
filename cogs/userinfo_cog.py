import discord
from discord.ext import commands
import datetime

class UserInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member : discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=False)
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No Roles", inline=False)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfoCog(bot))
