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
        start_time = time.time()
        message = await ctx.send("Pinging...")

        #calculate latency
        end_time = time.time()
        latency = (end_time - start_time) * 1000 #convert to ms

        #Edit message to include latency
        await message.edit(content=f"Pong! Ping: {int(latency)} ms")


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

        await ctx.send(f'Gateway Latency: {gateway_latency} ms \nREST API Latency: {rest_latency} ms')


async def setup(bot):
    await bot.add_cog(NetworkTools(bot))
