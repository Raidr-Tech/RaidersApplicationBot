import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, View, button
from discord import app_commands
from config import *

GUILD_ID = discord.Object(GUILD)


class Modal1(Modal, title="Raiders Application (1/2)"):
             discord_name = TextInput(label="Discord Name:", required=True)
             steam_name = TextInput(label="Steam Name:", required=True)
             steam_id = TextInput(label="Steam ID (64):", required=True)
             age = TextInput(label="Age:", required=True)
             hours_played = TextInput(label="Hours Played:", required=True)

             async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.send_message("Application submitted!", ephemeral=True)


class RaidersView(View):
    @discord.ui.button(label="Raiders Applications", style=discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Modal1())
    
    @discord.ui.button(label="Continue", style=discord.ButtonStyle.grey)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"Under Construction")
        #await interaction.response.send_modal(Modal2())

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def button_callback(self, interaciton: discord.Interaction, button: discord.ui.Button):
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
        view = RaidersView()
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="rootembed", description="This is a test")
    @app_commands.guilds(GUILD_ID)
    async def rootEmbed(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=PINK)
        embed.set_image(url='https://media.discordapp.net/attachments/1175019062942781450/1399018806155939950/image.png?ex=6887794b&is=688627cb&hm=98de898bee56316936d38c06913e59307a5a2c7f2c94972d900bdc49208e478a&=&format=webp&quality=lossless')
        view = RaidersView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(client):
    await client.add_cog(Commands(client=client))
