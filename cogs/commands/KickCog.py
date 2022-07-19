import discord
from discord.ext import commands

from utils import AdminEventTable

import psycopg2

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        if (member is not None):
            try:
                member.kick()
                insertedEvent = AdminEventTable.insert(str(member.id), str(member.guild.id), 'KICK', reason)
                await DiscordUtils.logToModlog(insertedEvent, member.guild)
                
                await ctx.reply(str(member) + ' has been kicked.')
            except (Exception, psycopg2.DatabaseError):
                await ctx.reply('Error kicking user. Contact bot developer/server administrator.')
        else:
            await ctx.reply('Member is required to kick. (ex. -kick @User)')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You are missing Kick Members permission(s) to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Invalid kick format. (ex. -kick @User reason)")

def setup(bot):
    bot.add_cog(KickCog(bot))