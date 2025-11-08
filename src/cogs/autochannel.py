import discord
from discord.ext import commands
import database


class Autochannel(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        db = database.DB
        channel_id = db.get_setting(member.guild.id, "voicechannel")
        category = self.bot.get_channel(db.get_setting(member.guild.id, "voicecategory"))

        if after.channel and after.channel.id == channel_id:
            channame = f"🎮 {member.activity.name}" if member.activity else f"💬 {member.name}"

            overwrite = discord.PermissionOverwrite(manage_channels=True, mute_members=True, move_members=True)

            newchan = await member.guild.create_voice_channel(
                name=channame,
                category=category,
                position=(len(category.voice_channels) + 1),
                overwrites={member: overwrite},
            )

            await member.move_to(channel=newchan)

            def emptycheck(m, b, a):
                return len(newchan.members) == 0

            await self.bot.wait_for("voice_state_update", check=emptycheck)
            await newchan.delete()


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Autochannel(bot))