import discord
from discord.ext import commands

from asyncio import sleep
from utils import AdminEventTable

import psycopg2

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason = None):
        try:
            muteRole = discord.utils.get(member.guild.roles, name = 'Muted')

            await member.add_roles(muteRole)
            AdminEventTable.insert(str(member.id), str(member.guild.id), 'MUTE', reason)

            await ctx.reply(f"{ member } has been muted for { duration } seconds.")

            await sleep(duration)

            muteRole = discord.utils.get(member.guild.roles, name = 'Muted')
            await member.remove_roles(muteRole)
        except (Exception, psycopg2.DatabaseError) as error:
            await ctx.reply('Error muting user. Contact bot developer/server administrator.')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You are missing Kick Members permission(s) to run this command.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Invalid mute format. (ex. -mute @User 60 reason)")

def setup(bot):
    bot.add_cog(MuteCog(bot))