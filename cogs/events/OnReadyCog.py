import discord
from discord.ext import commands

class OnReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bot = self.bot
        
        print(f'Logged in as { bot.user } (ID: { bot.user.id })')

def setup(bot):
    bot.add_cog(OnReadyCog(bot))