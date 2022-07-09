import discord

from utils import AdminEventTable, DiscordUtils

async def send_dm(member: discord.Member, content):
    dmChannel = await member.create_dm()
    await dmChannel.send(content)

async def doWarn(member, reason):
    dm_message = f"**Hello { member.name }!** You have received a warning { 'for the following reason: **' + reason + '**' if reason is not None else '' }. Make sure you look over our rules to prevent future infractions."
    await DiscordUtils.send_dm(member, dm_message)
    AdminEventTable.insert(str(member.id), str(member.guild.id), 'WARN', reason)