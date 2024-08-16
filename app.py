def print_banner():
    banner = """
#=====================================================================================#
#    _____                 ___ _        ____  _                   _    _____     _
#   |  _  |___ ___ ___ _ _|  _| |_ _   |    \|_|___ ___ ___ ___ _| |  | __  |___| |_
#   |   __| -_|  _|  _| | |  _| | | |  |  |  | |_ -|  _| . |  _| . |  | __ -| . |  _|
#   |__|  |___|_| |_| |_  |_| |_|___|  |____/|_|___|___|___|_| |___|  |_____|___|_|
#                     |___|
#
#                                 Developed by perryhu
#=====================================================================================#
"""
    print(banner)

# ================================
# Imports
# ================================
import os

import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv

import datetime

from dataclasses import dataclass
import random


# ================================
# Environment Variables
# ================================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD = os.getenv("DISCORD_GUILD") #https's server


# ================================
# Define Classes
# ================================
@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

#CREATE SESSION OBJECT
session = Session()


# ================================
# Bot Setup
# ================================
CHANNEL_ID = 1273278488618467328 #https's server -> #bot-dev

#DEFINE BOT PREFIX
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

#BOT DEVS USER IDs
WORKFLY_USER_ID = 757614271030100028
HTTPS_USER_ID = 784442224930324501

#BOOT_UP INITIAL MESSAGE
@bot.event
async def on_ready():
    print_banner()

    #Connect to specific guild (https's server)
    guild = discord.utils.get(bot.guilds, name=GUILD)

    #Confirmation Messages (command line)
    print(f'{bot.user.name} has successfully connected to Discord')
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    #List members in Guild
    members = '\n-'.join([member.name for member in guild.members])
    print(f'\nGuild Members:\n- {members}')

    channel = bot.get_channel(CHANNEL_ID) #text-channel #bot-dev
    #First Message when booted up
    await channel.send(f"Logged in as {bot.user.name}")



# ================================
# Command Handling
# ================================
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}")


@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)

    await ctx.send(f"Your sum equals: {result}")

#START A NEW SESSION
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True

    session.start_time = ctx.message.created_at.timestamp()
    readable_time = ctx.message.created_at.strftime("%H:%M:%S")

    await ctx.send(f"New session started at {readable_time}!")


# STOP EXISTING SESSION
@bot.command()
async def stop(ctx):
    if not session.is_active:
        await ctx.send("No session is active")
        return

    session.is_active = False

    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    readable_duration = str(datetime.timedelta(seconds=duration))

    await ctx.send(f"Session ended after {duration} seconds.")



# ================================
# Event Handling
# ================================
"""
#ECHO WORKFLY (No Prefix)
@bot.event
async def on_message(message):
    #prevent infinite loop
    if message.author == bot.user:
        return

    if message.content == "raise-exception":
        raise discord.DiscordExceptio #on_error function

    #**IMPORTANT MUST INCLUDE FOR COMMANDS TO WORK**
    #If message is a command, processes instead, if on_message function isn't applicable, move onto other commands
    author_name = message.author.name
    print("On message called, author: ", author_name)
    await bot.process_commands(message)

    #Check if message author is (not) workfly
    if message.author.id != HTTPS_USER_ID:
        print("user is not https")
        return
    else:
        print("echoing message from user: ", author_name)
        await message.channel.send(message.content)
"""


# ================================
# Error Handling
# ================================
@bot.event
async def on_error(event, *args, **kwargs):
    #use 'cat err.log' to access logs 
    with open('err.log', 'a') as f:
        #check if event that caused error was 'on_message'
        if event == 'on_message':
            f.write(f'Unhandeld message: {args[0]}\n')
        else:
            raise

@bot.event
async def on_command_error(ctx, error):
    #Get current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %A %H:%M:%S')

    with open('err.log', 'a') as f:
        f.write(f'[{timestamp}]Error with command {ctx.command}: {error}\n')
        await ctx.send(f'An error occured: {error}')


# ================================
# Run Bot
# ================================
bot.run(BOT_TOKEN)
