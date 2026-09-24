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


class Bot(commands.Bot):
    async def setup_hook(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')
                print(f"loaded {file}")


bot = Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Im ready!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
