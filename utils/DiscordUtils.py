import discord

from utils import AdminEventTable, DiscordUtils, GeneralUtils
from model.AdminEvent import AdminEvent

async def send_dm(member: discord.Member, content):
    dmChannel = await member.create_dm()
    await dmChannel.send(content)

async def doWarn(member: discord.Member, author: discord.Member, reason: str = None):
    dm_message = f"**Hello { member.name }!** You have received a warning { 'for the following reason: **' + reason + '**' if reason is not None else '' }. Make sure you look over our rules to prevent future infractions."
    await DiscordUtils.send_dm(member, dm_message)
    insertedEvent = AdminEventTable.insert(str(member.id), str(member.guild.id), str(author.id), 'WARN', reason)
    await logToModlog(insertedEvent, member.guild)

async def logToModlog(event: AdminEvent, guild: discord.Guild):
    modlogChannelName = GeneralUtils.getConfig('config.ini', 'guild')['modlogchannelname']
    modlogChannel = discord.utils.get(guild.text_channels, name = modlogChannelName)

    if modlogChannel is not None:
        formattedEvent = AdminEventTable.formatEvent(event)
        await modlogChannel.send(f"<@{ event.userID }> has been { formattedEvent['name'] } { 'for the following reason: **' + event.eventReason + '**' if event.eventReason is not None else '' }")