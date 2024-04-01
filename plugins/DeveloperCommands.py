from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

from api.view import BaseView
import api.permissions as perms

import uuid

__plugin__ = "Developer Commands"
__author__ = "OCbwoy3"

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='say',description='Make Skidisher Skidtru say anything you desire!')
		@app_commands.check(perms.is_ocbwoy3)
		@app_commands.describe(text='Text to send.')
		async def say_anything(interaction:Interaction,text:str):
			await interaction.response.send_message(text)

		registrate.misc.add_command(say_anything)

		@app_commands.command(name='prikolshub',description='Spawn a fake PrikolsHub session request.')
		async def prikolshub_session_request(interaction:Interaction):
			await interaction.response.defer(ephemeral=False,thinking=True)
			
			view = BaseView(user=None,timeout=None)

			accept = discord.ui.Button[BaseView](label='Accept',emoji='✅',style=discord.ButtonStyle.success,custom_id='accept',disabled=True)
			decline = discord.ui.Button[BaseView](label='Decline',emoji='❌',style=discord.ButtonStyle.danger,custom_id='decline',disabled=True)
			link = discord.ui.Button[BaseView](label="Visit Game",style=discord.ButtonStyle.link,url="https://www.roblox.com/games/843468296/Void-Script-Builder-Place-1")

			view.add_item(accept)
			view.add_item(decline)
			view.add_item(link)

			embed = discord.Embed(colour=discord.Colour.green(),title=f"Void Script Builder (Place 1)",description="A Roblox server has requested to create a session!",url=f"https://www.roblox.com/games/843468296/Void-Script-Builder-Place-1")
			embed.add_field(name='**PlaceId:**',value="843468296",inline=False)
			embed.add_field(name='**JobId:**',value=str(uuid.uuid4()),inline=False)
			view.message = await interaction.followup.send(f"Session Request Expires in 20 minutes.",view=view,embed=embed)

		registrate.misc.add_command(prikolshub_session_request)