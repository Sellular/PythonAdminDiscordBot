import discord
from discord.ext import commands

from utils import DiscordUtils, AdminEventTable

import psycopg2

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        if (member is not None):
            try:
                member.ban()
                dm_message = f"**Hello { member.name }!** You have received a banned from { ctx.guild.name }{ 'for the following reason: **' + reason + '**' if reason is not None else '' }."
                DiscordUtils.send_dm(member, dm_message)
                AdminEventTable.insert(str(member.id), str(member.guild.id), 'BAN', reason)
                await ctx.reply(str(member) + ' has been banned.')
            except (Exception, psycopg2.DatabaseError):
                await ctx.reply('Error banning user. Contact bot developer/server administrator.')
        else:
            await ctx.reply('Member is required to ban. (ex. -ban @User)')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You are missing Ban Members permission(s) to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Invalid ban format. (ex. -ban @User reason)")

def setup(bot):
    bot.add_cog(BanCog(bot))