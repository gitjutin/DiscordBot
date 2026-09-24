import random
from discord.ext import commands
import discord
import os

USER_IDS = [
    519679522392768523,  # Mary
    193776838974242818,  # Vanessa
    114226866461605897,  # Justin
    238120457923067905,  # Geeb
]


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='owen')
    async def owen(self, ctx):
        user_id = random.choice(USER_IDS)
        await ctx.send(f'Hey <@{user_id}>, do you know owen? :P')

    @commands.command(name='commands')
    async def commands_list(self, ctx):
        embed = discord.Embed(
            title="Bot Commands",
            description="Available commands:",
            color=discord.Color.blue()
        )
        embed.add_field(name="1️⃣ !owen", inline=False,
                        value="You know what it does")
        embed.add_field(name="2️⃣ !commands", inline=False,
                        value="Shows this list of commands")
        embed.add_field(name="3️⃣ !plug", inline=False,
                        value="Shows my Github, Resume, and Linkedin links")
        embed.add_field(name="4️⃣ !puff", inline=False,
                        value="Shows a picture of Puff!")
        await ctx.send(embed=embed)

    @commands.command(name='plug')
    async def plug(self, ctx):
        embed = discord.Embed(
            title="Plug",
            description="Check me out here:",
            color=discord.Color.purple()
        )
        embed.add_field(name="1️⃣ Github", inline=False,
                        value="[Check out my Github](https://github.com/gitjutin)")
        embed.add_field(name="2️⃣ Resume", inline=False,
                        value="[Check out my Resume](https://drive.google.com/file/d/1Z5VOdqTVHODuuFu47M3gDYO9LC8pWoAR/view?usp=sharing)")
        embed.add_field(name="3️⃣ Linkedin", inline=False,
                        value="[Check out my Linkedin](https://www.linkedin.com/in/justin-do-a96397207/)")
        embed.set_footer(text="Thanks for checking me out!")
        await ctx.send(embed=embed)

    @commands.command(name='puff')
    async def puff(self, ctx):

        images = [f for f in os.listdir("pics") if f.endswith(
            (".png", ".jpg", ".jpeg", ".gif"))]
        if not images:
            await ctx.send("No images found.")
            return

        random_pic = random.choice(images)
        ext = os.path.splitext(random_pic)[1]
        filename = f"pics{ext}"

        file = discord.File(os.path.join(
            "pics", random_pic), filename=filename)

        embed = discord.Embed(
            title="Puff Selfies", color=discord.Color.blue(), description="Hey it's me Puff!")
        embed.set_image(url=f"attachment://{filename}")
        await ctx.send(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Fun(bot))
