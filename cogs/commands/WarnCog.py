import discord
from discord.ext import commands

from utils import DiscordUtils

import psycopg2

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member: discord.Member, *, reason = None):
        try:
            await DiscordUtils.doWarn(member, ctx.author, reason)
            await ctx.reply(str(member) + ' has been warned.')
        except (Exception, psycopg2.DatabaseError):
            await ctx.reply('Error warning user. Contact bot developer/server administrator.')

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You are missing Kick Members permission(s) to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Invalid warn format. (ex. -warn @User reason)")

def setup(bot: commands.Bot):
    bot.add_cog(WarnCog(bot))