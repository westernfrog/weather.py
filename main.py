import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix="<prefix>", intents=discord.Intents.all())

for folder in os.listdir("./programs"):
    if folder.endswith(".py"):
        client.load_extension(f'programs.{folder[:-3]}')

token = "<token>"
client.run(token)
