import discord, os
from discord.ext import commands

def setupBot():
    description = 'An administration bot'

    intents = discord.Intents.default()
    intents.guild_messages = True
    intents.members = True
    intents.bans = True

    return commands.Bot(command_prefix=('-', '='), intents=intents, description=description)

def importCogs(bot: discord.ext.commands.Bot):
    for filename in os.listdir("./cogs/commands"):
        if filename.endswith(".py"):
            cogName = filename[:-3]
            bot.load_extension("cogs.commands." + cogName)

    for filename in os.listdir("./cogs/events"):
        if filename.endswith(".py"):
            cogName = filename[:-3]
            bot.load_extension("cogs.events." + cogName)