from discord.ext import commands
import discord
from config import token

intents = discord.Intents.all()
extensions = [
    "cogs.minesweeper",
    "cogs.controlcogs",
    "jishaku"
    ]

class Botkugo(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        print(f"Logged in as {bot.user.name} with ID {bot.user.id}")
        print("-------------------------------")

bot = Botkugo(command_prefix="!", intents=intents)

bot.run(token)