import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Enable intents for the bot from 'discord.com/developers/applications' -> bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.commands(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')
