import discord
from discord.ext import commands
import time
import aiohttp

class NetworkTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #PING COMMAND TEST FOR LATENCY (ms)
    @commands.command()
    async def ping(self, ctx):
        ping_embed = discord.Embed(title="Pong! :ping_pong:", description="Calculating...", color=discord.Color.orange())
        ping_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)


        #calculate latency
        start_time = time.time()
        message = await ctx.send(embed=ping_embed)
        end_time = time.time()

        round_trip_time = round((end_time - start_time) * 1000)
        latency = round((self.bot.latency * 1000))

        ping_embed.description = f"Ping: {latency} ms\nRound-trip: {round_trip_time} ms"
        ping_embed.color = discord.Color.green()

        await message.edit(embed=ping_embed)


    #LATENCY TEST COMMAND
    @commands.command()
    async def latency(self, ctx):
        #Gateway API Latency (=ping)
        gateway_latency = round(self.bot.latency * 1000)

        #REST API Latency
        url = "https://jsonplaceholder.typicode.com/todos/1" #Random link???
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.get(url) as response:
                end_time = time.time()
                rest_latency = round((end_time - start_time) * 1000)

        latency_embed = discord.Embed(title=f"{self.bot.user.name}'s Latency", color=0xff1414)
        latency_embed.add_field(name=f"Gateway API Latency: {gateway_latency} ms", value="", inline=False)
        latency_embed.add_field(name=f"REST API Latency: {rest_latency} ms", value="", inline=False)
        latency_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=latency_embed)


async def setup(bot):
    await bot.add_cog(NetworkTools(bot))
