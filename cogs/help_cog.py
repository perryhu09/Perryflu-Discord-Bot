import discord
from discord.ext import commands

EMBEDS_COLOR = 0x7a450c

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        embed = discord.Embed(
            title = "Perryflu Help Page",
            description = """
            ### Other Commands
            - **/help** - Show this help page
            - **/ping** - Get the ping of the bot
            - **/latency** - Details on latency of bot
            - **/start** - to remove
            - **/stop** - to remove
            """,
            color = EMBEDS_COLOR
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
