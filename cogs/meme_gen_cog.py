import discord
from discord.ext import commands

from random import choice
import asyncpraw as praw

class MemeGenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
        client_id="34tz2yYmox_54MX84qcawg",
        client_secret="dW6RKNHcwg8Y1MfzAjJTkFHSvL9e_A",
        user_agent="script:meme_gen:v1.0 (by u/perry_hu)"
        )

    @commands.command()
    async def meme(self, ctx: commands.Context):

        subreddit = await self.reddit.subreddit("ProgrammerHumor")
        posts_list = []

        async for post in subreddit.hot(limit=50):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "no poster"))

        if posts_list:
            random_post = choice(posts_list)

            meme_embed = discord.Embed(
            title=f"Random meme",
            description="Random meme from r/ProgrammerHumor on reddit",
            color=discord.Color.random())

            meme_embed.set_author(name=f"Meme reqeuested by {ctx.author.name}", icon_url=ctx.author.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Post created by {random_post[1]}", icon_url=None)

            await ctx.send(embed=meme_embed)

        else:
            await ctx.send("Unable to fetch meme, try again later")


    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())

async def setup(bot):
    await bot.add_cog(MemeGenCog(bot))
