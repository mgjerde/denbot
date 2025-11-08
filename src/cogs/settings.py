# import configparser
import discord
import database
from discord.ext import commands

# config = configparser.ConfigParser()
# config.read('settings.ini')


class SettingButton(discord.ui.Button):
    def __init__(self, label, identifier, data):
        """A button for one role. `custom_id` is needed for persistent views."""
        super().__init__(
            label=label,
            style=discord.ButtonStyle.primary,
            custom_id=str(identifier),
        )
        self.data = data

    async def callback(self, interaction: discord.Interaction):
        """
        This function will be called any time a user clicks on this button.

        Parameters
        ----------
        interaction: :class:`discord.Interaction`
            The interaction object that was created when a user clicks on a button.
        """
        dropdown = Dropdown(self)
        dropdown.custom_id = self.custom_id
        for x in self.data:
            dropdown.add_option(label=x.name, value=str(x.id))
        buttonview = discord.ui.View(timeout=None)
        buttonview.add_item(dropdown)

        await interaction.response.send_message(
            view=buttonview,
            ephemeral=True,
        )


class Dropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            min_values=1,
            max_values=1,
            options=[],
        )

    async def callback(self, interaction: discord.Interaction):
        # config[interaction.guild_id] = {self.custom_id: self.values[0]}
        db = database.DB
        db.update_setting(interaction.guild_id, self.custom_id, self.values[0])
        await interaction.response.edit_message(
            view=None,
            content=f"{self.custom_id} saved as {self.values[0]}",
            delete_after=5,
        )


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="setup", description="Setup settings for the server")
    async def setup_command(
        self,
        ctx: discord.ApplicationContext,
    ):
        settingsview = discord.ui.View(timeout=None)
        settingsview.add_item(
            SettingButton("Auto role on join", "autorole", ctx.guild.roles)
        )
        settingsview.add_item(
            SettingButton("Looking for group role", "lfgrole", ctx.guild.roles)
        )
        settingsview.add_item(
            SettingButton("Automatic voice", "voicechannel", ctx.guild.voice_channels)
        )
        settingsview.add_item(
            SettingButton("Currently Streaming", "streamingrole", ctx.guild.roles)
        )
        settingsview.add_item(
            SettingButton("Event channel", "eventchannel", ctx.guild.text_channels)
        )
        settingsview.add_item(
            SettingButton("Voice channel category", "voicecategory", ctx.guild.categories)
        )

        await ctx.response.send_message(
            view=settingsview, ephemeral=True
        ) if ctx.author == ctx.guild.owner else await ctx.response.send_message(
            "Only the server administrator can run this command!", ephemeral=True
        )


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))
