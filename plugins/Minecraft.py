from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

from api.view import BaseView
import api.permissions as perms

__plugin__ = "Minecraft Server"
__author__ = "OCbwoy3"

import os
from exaroton import Exaroton

client = Exaroton(os.getenv('EXAROTON_TOKEN'))

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='console',description='Run something in the console.')
		@app_commands.check(perms.is_ocbwoy3)
		@app_commands.describe(command='The command to execute in the Console.')
		async def console(interaction:Interaction,command:str):
			await interaction.response.defer(ephemeral=False,thinking=True)
			res = client.command(os.getenv('SERVER_ID'),command)
			await interaction.followup.send(f"Response from Exaroton API: `{res}`",ephemeral=False)

		registrate.mc.add_command(console)

		@app_commands.command(name='start',description='Start the server.')
		@app_commands.check(perms.is_ocbwoy3)
		async def start(interaction:Interaction):
			await interaction.response.defer(ephemeral=False,thinking=True)
			res = client.start(os.getenv('SERVER_ID'))
			await interaction.followup.send(f"Response from Exaroton API: `{res}`",ephemeral=False)

		registrate.mc.add_command(start)

