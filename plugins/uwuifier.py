from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

import uwuipy
import api.permissions as perms

__plugin__ = "uwuifier"
__author__ = "OCbwoy3"

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='uwuify',description='uwuifies the provided text.')
		@app_commands.check(perms.is_whitelisted)
		@app_commands.describe(text='Text to uwuify',nsfw='Define if NSFW results should be outputted',ephmereal='Shows the message only for you')
		async def uwuify_command(interaction:Interaction,text:str,nsfw:bool=False,ephmereal:bool=False):
			await interaction.response.defer(ephemeral=ephmereal,thinking=True)
			uwuifier = uwuipy.uwuipy(nsfw_actions=nsfw)
			await interaction.followup.send(uwuifier.uwuify(text))
				
		registrate.fun.add_command(uwuify_command)