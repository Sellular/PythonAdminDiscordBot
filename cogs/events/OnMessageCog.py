import discord
from discord.ext import commands

import re

from utils import DiscordUtils

discordInviteFilter = re.compile("(...)?(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")

class OnMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        bot = self.bot

        if discordInviteFilter.match(message.content):
            await message.delete()
            await message.channel.send(f"<@{ message.author.id }> :no_entry: Advertising is not allowed! Please read our rules found in #our-rules")
            await DiscordUtils.doWarn(message.author, "Advertising")

def setup(bot):
    bot.add_cog(OnMessageCog(bot))