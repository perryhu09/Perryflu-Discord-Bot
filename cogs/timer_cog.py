import discord
from discord.ext import commands
import asyncio
import time

class TimerView(discord.ui.View):
    def __init__(self, seconds, cog):
        super().__init__()
        self.seconds = seconds
        self.cog = cog
        self.message = None
        self.cancelled = False


    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        await self.cog.start_timer(self, interaction, self.message, self.seconds)


    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog.cancel_timer(self, interaction, self.message)


class TimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def timer(self, ctx, seconds: int):
        if seconds <= 0:
            await ctx.send("Please enter a time in seconds greater than 0.")
            return

        embed = discord.Embed(title=f"{ctx.author.name}'s Timer",
        description=f"Timer for {seconds} seconds.\nClick the start button to start the timer.",
        color=discord.Color.green())

        view = TimerView(seconds, self)

        message = await ctx.send(embed=embed, view=view)
        view.message = message

    async def start_timer(self, view: TimerView, interaction, message, seconds):
        while seconds and not view.cancelled:
            minutes, secs = divmod(seconds, 60)
            time_format = '{:02d}:{:02d}'.format(minutes, secs)
            embed = discord.Embed(title=f"{interaction.user.name}'s Timer", description=f"Time remaining: {time_format}", color=discord.Color.yellow())
            await message.edit(embed=embed)
            await asyncio.sleep(1)
            seconds -= 1

        if not view.cancelled:
            await self.time_up(view, interaction, message)


    async def time_up(self, view: TimerView, interaction, message):
        embed = discord.Embed(title=f"{interaction.user.name}'s Timer",
        description=f"Time's Up", color=discord.Color.red())
        await self.disable_all_buttons(view)
        await message.edit(embed=embed)
        await interaction.channel.send(f"{interaction.user.mention} Your timer has ended!")


    async def cancel_timer(self, view: TimerView,  interaction, message):
        view.cancelled = True

        embed = discord.Embed(title=f"{interaction.user.name}'s Timer", description=f"Timer has been canceled", color=discord.Color.red())
        await self.disable_all_buttons(view)

        await message.edit(embed=embed)

        #await interaction.response.send_message(f"{interaction.user.mention} Your timer has been canceled.")

    async def disable_all_buttons(self, view: TimerView):
        for item in view.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        if view.message:
            await view.message.edit(view=view)

async def setup(bot):
    await bot.add_cog(TimerCog(bot))
