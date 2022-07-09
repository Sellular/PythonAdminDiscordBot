import discord
from discord.ext import commands

from datetime import datetime

class UserinfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member):
        try:
            embed = discord.Embed (
                color = discord.Color(0xff3400),
                title = f"Member information { member }"
            )

            embed.add_field(name = "**Nickname**", value = f"{ member.display_name }", inline = True)

            embed.add_field(name = "**ID**", value = f"{ member.id }", inline = True)

            botValue = "Yes" if member.bot else "Unlikely"
            embed.add_field(name = "**Is Bot**", value = botValue, inline = True)
            embed.set_thumbnail(url = f"{ member.avatar_url }")

            embed.add_field(name = "**Joined Server**", value = f"{ member.joined_at.strftime('%a') } { member.joined_at.strftime('%b') } { member.joined_at.day } { member.joined_at.hour }:{ member.joined_at.minute }:{ member.joined_at.second } \n{ member.joined_at.year } \n(<t:{ int(member.joined_at.timestamp()) }:R>)".replace("-", "/"), inline = True)
            embed.add_field(name = "**Joined Discord**", value = f"{ member.created_at.strftime('%a') } { member.created_at.strftime('%b') } { member.created_at.day } { member.created_at.hour }:{ member.created_at.minute }:{ member.created_at.second } \n{ member.created_at.year } \n(<t:{ int(member.created_at.timestamp()) }:R>)".replace("-", "/"), inline = True)
            embed.add_field(name = "**Avatar URL**", value = f"[Click to open]({ member.avatar_url })", inline = True)

            embed.set_footer(icon_url = f"{ ctx.author.avatar_url }", text = f"Requested by { ctx.author }")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed = embed)
        except (Exception) as error:
            print(error)
            await ctx.reply("Error obtaining user info. Contact bot developer/server administrator.")

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Invalid userinfo format. (ex. -userinfo @User)")

def setup(bot):
    bot.add_cog(UserinfoCog(bot))