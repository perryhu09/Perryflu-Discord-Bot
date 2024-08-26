import discord
from discord.ext import commands

EMBEDS_COLOR = 0x7a450c

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx):
        bot_avatar_url = self.bot.user.avatar.url

        embed = discord.Embed(
            title = "Perryflu Help Page",
            description = """
            ## Commands
            - **/helpme** - Show this help page
            - **/timer {seconds}** - sets a timer for specified number of seconds
            - **/userinfo** - Get information on a specific user
            - **/meme** - fetch random meme from r/ProgrammingHumour
            - **/ping** - Get the ping of the bot
            - **/latency** - Details on latency of bot
            - **/balance** - [eco] display your balance
            - **/work** - [eco] earn some cash
            - **/beg** - [eco] try begging for money
            """,
            color = EMBEDS_COLOR
        )
        embed.set_thumbnail(url=bot_avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
