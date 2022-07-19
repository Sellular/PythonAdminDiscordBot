import discord
from discord.ext import commands
import psycopg2

from utils import AdminEventTable

class EditWarningCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('Moderator', 'Admin')
    async def editwarning(self, ctx: commands.Context, eventID: int, *, reason):
        isMod = discord.utils.get(ctx.author.roles, name = 'Moderator')

        userEvent = None

        try:
            userEvent = AdminEventTable.getEventById(eventID)

            if userEvent is None:
                await ctx.reply(f'Case number {eventID} does not exist.')
                return

            if userEvent.eventCode != 'WARN':
                await ctx.reply('Infraction is not a warning.')
                return

            if userEvent.eventReason == 'Advertising':
                await ctx.reply('Cannot modify advertising warning')
                return

            if isMod and userEvent.submittedUserID != str(ctx.author.id):
                await ctx.reply('You cannot edit a case that is not your own.')
                return

            AdminEventTable.updateEventById(eventID, reason)
            await ctx.reply('Warning reason has been updated.')
            
        except (Exception, psycopg2.DatabaseError):
            await ctx.reply('Error editing history case. Contact bot developer/server administrator.')

    @editwarning.error
    async def editwarning_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Invalid editwarning format. (ex. -editwarning ID reason)')
        if isinstance(error, commands.MissingAnyRole):
            await ctx.reply("You are missing Moderator or Admin role(s) to run this command.")

def setup(bot):
    bot.add_cog(EditWarningCog(bot))