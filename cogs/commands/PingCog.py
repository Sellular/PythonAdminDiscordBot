import discord
from discord.ext import commands

from datetime import datetime
from time import sleep

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        bot = self.bot

        calculatingEmbed = discord.Embed(
            color = discord.Color(0xff3400),
            title = "Pong!",
            description = "Calculating...\n"
        )

        calculatingEmbed.timestamp = datetime.utcnow()
        sentMessage = await ctx.reply(embed = calculatingEmbed)

        sleep(1)

        pingEmbed = discord.Embed(
            color = discord.Color(0xff3400)
        )

        pingEmbed.set_author(name = f"{ bot.user }", icon_url = bot.user.avatar_url)

        pingEmbed.add_field(name = "Ping", value = f"**{ round(bot.latency * 1000) }** ms")
        
        pingEmbed.set_footer(icon_url = f"{ ctx.author.avatar_url }", text = f"{ ctx.author }")
        pingEmbed.timestamp = datetime.utcnow()

        await sentMessage.edit(embed = pingEmbed)

def setup(bot):
    bot.add_cog(PingCog(bot))