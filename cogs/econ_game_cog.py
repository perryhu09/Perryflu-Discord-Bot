import discord
from discord.ext import commands
import json
import random


class EconGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member=None):

        member = member or ctx.author

        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

            if str(member.id) not in user_eco:
                user_eco[str(member.id)] = {}
                user_eco[str(member.id)]["Balance"] = 100

            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        eco_embed = discord.Embed(title=f"{member.name}'s Current Balance", color=discord.Color.green())
        eco_embed.add_field(name="Current Balance", value=f"${user_eco[str(member.id)]['Balance']}.")
        eco_embed.set_footer(text="Run /work to increase your balance!", icon_url=None)

        await ctx.send(embed=eco_embed)


    @commands.command()
    async def work(self, ctx):

        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

            if str(ctx.author.id) not in user_eco:
                user_eco[str(member.id)] = {}
                user_eco[str(member.id)]["Balance"] = 100

            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        diff = random.randint(100, 500)
        user_eco[str(ctx.author.id)]["Balance"] += diff

        eco_embed = discord.Embed(
        title="Zam!",
        description="After you 'worked' so hard at your job, you finally gained some money!",
        color=discord.Color.green()
        )
        eco_embed.add_field(name="Earnings: ", value=f"${diff}", inline=False)
        eco_embed.add_field(name="New Balance: ",
        value=f"{user_eco[str(ctx.author.id)]['Balance']}")

        await ctx.send(embed=eco_embed)

        with open("cogs/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)


    @commands.command()
    async def beg(self, ctx):

        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

            if str(ctx.author.id) not in user_eco:
                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100

            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

            cur_bal = user_eco[str(ctx.author.id)]["Balance"]
            diff = random.randint(-10, 30)
            new_bal = cur_bal + diff

            if cur_bal > new_bal:
                eco_embed = discord.Embed(
                title="Oh No! - You've been robbed",
                description="A group of robbers saw an opportunity in taking advantage of you.",
                color=discord.Color.red()
                )
                eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
                eco_embed.set_footer(text="You should probably get out of the hood", icon_url=None)

                await ctx.send(embed=eco_embed)

                user_eco[str(ctx.author.id)]["Balance"] += diff

                with open("cogs/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            elif cur_bal < new_bal:
                eco_embed = discord.Embed(
                title="Yessir!!!",
                description="Some people saw how broke ur ahh was and decided to help you a little.",
                color=discord.Color.green()
                )
                eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
                eco_embed.set_footer(text="You should probably get a job so u can stop begging on the streets", icon_url=None)

                await ctx.send(embed=eco_embed)

                user_eco[str(ctx.author.id)]["Balance"] += diff

                with open("cogs/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            elif cur_bal == new_bal:
                eco_embed = discord.Embed(title="Aw Dang it!",
                description="No one wanted to help ur broke ahh.",
                color=discord.Color.yellow(), inline=False)
                eco_embed.set_footer(text="Try again later :/", icon_url=None)
                await ctx.send(embed=eco_embed)

async def setup(bot):
    await bot.add_cog(EconGameCog(bot))
