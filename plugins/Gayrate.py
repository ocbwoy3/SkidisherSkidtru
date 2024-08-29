from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

import uwuipy
import api.permissions as perms

__plugin__ = "gayrate"
__author__ = "OCbwoy3"

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='gayrate',description='copy of heist\'s gayrate')
		@app_commands.check(perms.is_whitelisted)
		@app_commands.describe(user='gayrate user')
		async def gayrate(interaction:Interaction,user:discord.User):
			await interaction.response.defer(ephemeral=False,thinking=True)
			import random
			gay = random.randint(0,10000)/100
			if str(user.id) == "486147449703104523": gay = 10000
			if str(user.id) == "1015304151133077505": gay = 10000
			if str(user.id) == "479160987799257089": gay = 10000
			m = "😑"
			if gay >= 25:
				m = "😐"
			if gay >= 50:
				m = "🔥"
			if gay >= 75:
				m = "🏳️‍🌈"
			await interaction.followup.send(f"<@{user.id}> is {gay}% gay {m}")
				
		registrate.fun.add_command(gayrate)