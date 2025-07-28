import discord
import os
import logging
from dotenv import load_dotenv
from os import getenv
from config import *
from discord.ext import commands
from discord import app_commands

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
                command_prefix="+",
                intents=discord.Intents.all()
        )

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    print("Loading: cogs." + filename[:-3])
                    await self.load_extension("cogs." + filename[:-3])

        try:
            guild = discord.Object(id=722925148847472830)
            synced = await self.tree.sync(guild=guild)
            print(f'Successfully added {len(synced)} slash commands to guild {guild.id}')
        except Exception as e:
            print(f'Error loading slash commands: {e}')

    async def on_ready(self):
        print(f'Connected as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)

client = Client()


client.run(getenv("BOT_TOKEN"))
