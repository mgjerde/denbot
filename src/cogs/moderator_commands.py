from discord import colour, Embed
from discord.ext.commands import context
from discord.ext import commands
from discord.member import Member
from discord.commands import Option
from discord.commands import permissions
from discord.utils import get
from asyncio import sleep
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()
MODERATOR_ROLE = getenv('MODERATOR_ROLE')
WARNED_ROLE = getenv('WARNED_ROLE')


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.slash_command(default_permission=False, name="warn", description="Warn user and put them in temporary jail")
    @permissions.has_role(f"{MODERATOR_ROLE}")
    async def warn(
                    self, 
                    ctx: context,
                    user: Option(Member, "What user?", Required=True),
                    length: Option(str,"For how long?",choices=["15s","1m","5m","30m","1h"]),
                    reasoning: Option(str, "Why are they getting a warning?")
                ):
        if length == "15s": 
            waittime = 15
        elif length == "1m":
            waittime = 60
        elif length == "5m":
            waittime = 300
        elif length == "30m":
            waittime = 1800
        elif length == "1h":
            waittime = 3600
        else:
            waittime = 1 # Should not happend but just incase for now
        
        warned_role_obj = get( user.guild.roles, name=WARNED_ROLE )
        if not warned_role_obj:
            return
        await user.add_roles(warned_role_obj, reason=reasoning )

        if ctx.author.avatar:
            iconurl = ctx.author.avatar.url
        else:
            iconurl = ""

        warnembed = Embed(title="Warning!", description=f"{user.mention} has been warned for {reasoning}", colour=colour.Color.yellow(), timestamp=datetime.now())
        warnembed.set_footer(text="Duration: " + length,icon_url=iconurl)
        message = await ctx.respond(embed = warnembed,delete_after = waittime + 15)
        await sleep(waittime)
        
        warnembed.set_footer(text="Completed!",icon_url=iconurl)
        warnembed.colour=colour.Color.green()
        await message.edit_original_message(embed=warnembed)

        await user.remove_roles(warned_role_obj, reason=reasoning )
        
def setup(bot: commands.Bot):
    bot.add_cog(Moderator(bot))