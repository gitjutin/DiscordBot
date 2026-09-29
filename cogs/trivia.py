import aiohttp
import random
from discord.ext import commands

from views import AnswerView
import discord
from database import init_db, get_top, get_score

BASE = "https://ddragon.leagueoflegends.com"


async def load_champions():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE}/api/versions.json") as r:
            version = (await r.json())[0]   # newest patch
        async with session.get(f"{BASE}/cdn/{version}/data/en_US/championFull.json") as r:
            data = await r.json()
    return list(data["data"].values()), version


def title_question(champions):
    correct, *wrong = random.sample(champions, 4)   # 4 unique champions
    answers = [c["name"] for c in [correct, *wrong]]
    random.shuffle(answers)
    return {
        "question": f"Which champion is known as {correct['title']}?",
        "answers": answers,
        "correct": correct["name"],
    }


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.champions = []
        self.version = None

    async def cog_load(self):
        await init_db()
        self.champions, self.version = await load_champions()
        print(f"Loaded {len(self.champions)} champions (patch {self.version})")

    @commands.command(name="trivia", help="Starts a trivia round")
    @commands.guild_only()
    async def trivia(self, ctx):
        q = title_question(self.champions)
        view = AnswerView(q["answers"], q["correct"])
        view.message = await ctx.send(q["question"], view=view)

    @commands.command(name="leaderboard", aliases=["lb"], help="Shows the trivia leaderboard")
    @commands.guild_only()
    async def leaderboard(self, ctx):
        rows = await get_top(ctx.guild.id)
        if not rows:
            await ctx.send("No scores yet! Start a round with `!trivia`.")
            return

        medals = ["🥇", "🥈", "🥉"]
        lines = []
        for i, (user_id, points) in enumerate(rows):
            rank = medals[i] if i < 3 else f"`#{i + 1}`"
            label = "pt" if points == 1 else "pts"
            lines.append(f"{rank} <@{user_id}> — **{points}** {label}")

        embed = discord.Embed(
            title="🏆 Trivia Leaderboard",
            description="\n".join(lines),
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="score", help="Shows your current trivia score")
    @commands.guild_only()
    async def score(self, ctx):
        points = await get_score(ctx.guild.id, ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, you have **{points}** point(s).")


async def setup(bot):
    await bot.add_cog(Trivia(bot))
