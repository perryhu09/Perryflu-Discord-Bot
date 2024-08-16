import discord
from discord.ext import commands

import time
import datetime

from classes.session import Session

class SessionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = Session()

    #START A NEW SESSION
    @commands.command()
    async def start(self, ctx):
        if self.session.is_active:
            await ctx.send("A session is already active!")
            return

        self.session.is_active = True
        self.session.start_time = ctx.message.created_at.timestamp()
        readable_time = ctx.message.created_at.strftime("%H:%M:%S")

        await ctx.send(f"New session started at {readable_time}!")


    # STOP EXISTING SESSION
    @commands.command()
    async def stop(self, ctx):
        if not self.session.is_active:
            await ctx.send("No session is active")
            return

        self.session.is_active = False
        end_time = ctx.message.created_at.timestamp()
        duration = end_time - self.session.start_time
        readable_duration = str(datetime.timedelta(seconds=duration))

        await ctx.send(f"Session ended after {duration} seconds.")

async def setup(bot):
    await bot.add_cog(SessionCog(bot))
