import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, View, button
from discord import app_commands
from config import *

GUILD_ID = discord.Object(GUILD)
user_applications = {}

class Modal1(Modal):
    def __init__(self):
        super().__init__(title="Raiders Application (1/2)")

        self.add_item(TextInput(label="Discord Name", required=True))
        self.add_item(TextInput(label="Steam Name", required=True))
        self.add_item(TextInput(label="Steam ID (64)", required=True))
        self.add_item(TextInput(label="Age", required=True))
        self.add_item(TextInput(label="Hours Played", required=True))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            data = {
                    "Discord Name": self.children[0].value,
                    "Steam Name": self.children[1].value,
                    "Steam ID 64": self.children[2].value,
                    "Age": self.children[3].value,
                    "Hours Played": self.children[4].value
            }

            user_applications[interaction.user.id] = data
            embed = discord.Embed(colour=PINK, title="Almost there!", description="You just finished 5 of the 8 questions we need to ask you.")
            embed.set_footer(text="Click the Continue button to resume.")
            view = RaidersView(buttons=["Continue", "Cancel"])
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            print(f"Error in Modal1: {e}")

class Modal2(Modal):
    def __init__(self, modal1_data: dict):
        super().__init__(title="Raiders Application (2/2)")
        self.modal1_data = modal1_data

        self.add_item(TextInput(label="Timezone", required=True))
        self.add_item(TextInput(label="Where did you hear of us?", style=discord.TextStyle.paragraph, required=True))
        self.add_item(TextInput(label="Why do you want to join us?", style=discord.TextStyle.paragraph, required=True))
    async def on_submit(self, interaction: discord.Interaction):
        try:
            timezone = self.children[0].value
            heard_from = self.children[1].value
            reason = self.children[2].value

            full_data = self.modal1_data.copy()
            full_data.update({
                "Timezone": timezone,
                "Where did you hear of us?": heard_from,
                "Why do you want to join us?": reason
            })

            user_applications.pop(interaction.user.id, None)

            print(full_data)
        except Exception as e:
            print(f"Error in Modal2: {e}")

class RaidersView(View):
    def __init__(self, buttons: list[str] = None, timeout=180):
        super().__init__(timeout=timeout)
        buttons = buttons or []

        if "Raiders Applications" in buttons:
            self.add_item(RaidersApplicationButton())

        if "Continue" in buttons:
            self.add_item(ContinueButton())

        if "Cancel" in buttons:
            self.add_item(CancelButton())

class RaidersApplicationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Raiders Applications", style=discord.ButtonStyle.red)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Modal1())
    
class ContinueButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Continue", style=discord.ButtonStyle.grey)
    async def callback(self, interaction: discord.Interaction):
        modal1_data = user_applications.get(interaction.user.id)
        if not modal1_data:
            await interaction.response.send_message("An error has occured, please contact a staff member.", ephemeral=True)
            return
        print(f"Under Construction")
        await interaction.response.send_modal(Modal2(modal1_data))

class CancelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Cancel", style=discord.ButtonStyle.red)
    async def callback(self, interaciton: discord.Interaction):
        print(f"Under Construction")
        # Needs to edit original embed to say "Cancelled Successfully!"

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="rootEmbed")
    @commands.has_any_role(TECHSEER)
    async def createApply(self, ctx):
        embed = discord.Embed(colour=PINK, title="Apply here!")
        embed.set_image(url='https://cdn.discordapp.com/attachments/1175019062942781450/1399018806155939950/image.png?ex=6887794b&is=688627cb&hm=98de898bee56316936d38c06913e59307a5a2c7f2c94972d900bdc49208e478a&')
        view = RaidersView(buttons=["Raiders Applications"])
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="rootembed", description="This is a test")
    @app_commands.guilds(GUILD_ID)
    async def rootEmbed(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=PINK)
        embed.set_image(url='https://media.discordapp.net/attachments/1175019062942781450/1399018806155939950/image.png?ex=6887794b&is=688627cb&hm=98de898bee56316936d38c06913e59307a5a2c7f2c94972d900bdc49208e478a&=&format=webp&quality=lossless')
        view = RaidersView(buttons=["Raiders Applications"])
        await interaction.response.send_message(embed=embed, view=view)

async def setup(client):
    await client.add_cog(Commands(client=client))
