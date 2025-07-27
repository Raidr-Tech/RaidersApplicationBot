import discord
from discord.ext import commands
from discord import app_commands
from config import *

GUILD_ID = discord.Object(GUILD)

class View(discord.ui.View):
    @discord.ui.button(label="Raiders Applications", style=discord.ButtonStyle.red)
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("Testing!")

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="rootEmbed")
    @commands.has_any_role(TECHSEER)
    async def createApply(self, ctx):
        embed = discord.Embed(colour=PINK, title="Apply here!")
        embed.set_image(url='https://cdn.discordapp.com/attachments/1175019062942781450/1399018806155939950/image.png?ex=6887794b&is=688627cb&hm=98de898bee56316936d38c06913e59307a5a2c7f2c94972d900bdc49208e478a&')
        view = View()
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="rootembed", description="This is a test")
    @app_commands.guilds(GUILD_ID)
    async def rootEmbed(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=PINK)
        embed.set_image(url='https://media.discordapp.net/attachments/1175019062942781450/1399018806155939950/image.png?ex=6887794b&is=688627cb&hm=98de898bee56316936d38c06913e59307a5a2c7f2c94972d900bdc49208e478a&=&format=webp&quality=lossless')
        view = View()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(client):
    await client.add_cog(Commands(client=client))
