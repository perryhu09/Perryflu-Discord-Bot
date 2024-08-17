def print_banner():
    banner = """
=========================================================================================
     _____                 ___ _        ____  _                   _    _____     _
    |  _  |___ ___ ___ _ _|  _| |_ _   |    \|_|___ ___ ___ ___ _| |  | __  |___| |_
    |   __| -_|  _|  _| | |  _| | | |  |  |  | |_ -|  _| . |  _| . |  | __ -| . |  _|
    |__|  |___|_| |_| |_  |_| |_|___|  |____/|_|___|___|___|_| |___|  |_____|___|_|
                      |___|

                                  Developed by perryhu
=========================================================================================
"""
    print(banner)

# ================================
# Imports
# ================================
import os

import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
import asyncio

from itertools import cycle


# ================================
# Environment Variables
# ================================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD = os.getenv("DISCORD_GUILD") #https's server
CHANNEL_ID = int(os.getenv("CHANNEL_ID")) #bot-dev
HTTPS_USER_ID = int(os.getenv("HTTPS_USER_ID"))

# ================================
# Bot Setup
# ================================

#DEFINE BOT PREFIX
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

bot_status = cycle(["/helpme"]) #add more status' to cycle later

@tasks.loop(seconds=5)
async def change_status():
       await bot.change_presence(activity=discord.Game(next(bot_status)))

#BOOT_UP
@bot.event
async def on_ready():
    print_banner()

    #Connect to specific guild
    guild = discord.utils.get(bot.guilds, name=GUILD)

    #Confirmation Messages
    print(f'{bot.user.name} has successfully connected to Discord')
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    #List members in Guild
    members = '\n- '.join([member.name for member in guild.members])
    print(f'\nGuild Members:\n- {members}')

    change_status.start()

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Logged in as {bot.user.name}")

#SHUT DOWN THE BOT
@bot.command()
async def kill(ctx):
    print("Shutting Down...")
    if ctx.author.id == HTTPS_USER_ID:
        await ctx.send("Shutting Down...")
        await bot.close()
    else:
        await ctx.send("You do not have permission to use this command.")

#LOAD COGS
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded extension {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

#MAIN FUNCTION
async def main():
    async with bot:
        await load()
        await bot.start(BOT_TOKEN)

#RUN MAIN
asyncio.run(main())
