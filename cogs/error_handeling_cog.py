import discord
from discord.ext import commands
import time
import datetime

log_path = "./logs/err.log"

class ErrorHandelingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %A %H:%M:%S')

        with open(log_path, 'a') as f:
            #check if event that caused error was 'on_message'
            if event == 'on_message':
                f.write(f'[{timestamp}] Unhandeld message: {args[0]}\n')
            else:
                raise

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #Get current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %A %H:%M:%S')

        with open(log_path, 'a') as f:
            f.write(f'[{timestamp}] Error with command {ctx.command}: {error}\n')
            await ctx.send(f'An error occured: {error}')


async def setup(bot):
    await bot.add_cog(ErrorHandelingCog(bot))
