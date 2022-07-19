import discord
from discord.ext import commands

from utils import AdminEventTable

import psycopg2

class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def history(self, ctx, member: discord.Member, limit: int = 20):
        userEvents = None

        try:
            userEvents = AdminEventTable.getEventsByUserAndGuild(str(member.id), str(member.guild.id), limit)
        except (Exception, psycopg2.DatabaseError):
            await ctx.reply('Error obtaining user history. Contact bot developer/server administrator.')
            return

        if userEvents is None or len(userEvents) == 0:
            await ctx.reply('User has a clean record.')
            return

        embed = discord.Embed (
            color = discord.Color(0xff3400),
            title = f"{ member } History"
        )
        embed.set_thumbnail(url = f"{ member.avatar_url }")

        for event in userEvents:
            embedParms = AdminEventTable.formatEvent(event)

            embedValue = f"{ embedParms['timestamp'] }"
            if embedParms['reason'] is not None:
                embedValue = f"{ embedParms['reason'] } -- { embedValue }"

            embed.add_field(name = f'{ embedParms["name"]} - { embedParms["eventID"] }', value = embedValue, inline = False)

        await ctx.send(embed = embed)

    @history.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Invalid history format. (ex. -history @User 10)")

def setup(bot):
    bot.add_cog(HistoryCog(bot))