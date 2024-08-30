from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

import uwuipy
import api.permissions as perms

__plugin__ = "gayrate"
__author__ = "OCbwoy3"

global CACHE
CACHE = {}

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='gayrate',description='copy of heist\'s gayrate')
		# @app_commands.check(perms.is_whitelisted)
		@app_commands.describe(user='gayrate user')
		async def gayrate(interaction:Interaction,user:discord.User=None):
			await interaction.response.defer(ephemeral=False,thinking=True)
			global CACHE
			if user == None: user = interaction.user
			if str(user.id) == "1220838242270580737":
				await interaction.followup.send("wtf?")
				return
			import random
			gay = random.randint(0,10000)/100
			if str(user.id) == "486147449703104523": gay = 100
			if str(user.id) == "1015304151133077505": gay = 100
			if str(user.id) == "479160987799257089": gay = 100
			if str(user.id) == "458354633598042142": gay = 100
			gay2 = CACHE.get(user.id,None)
			if gay2 == None:
				CACHE[user.id]=gay
			else:
				gay = gay2
			
			m = "😑"
			if gay >= 25: m = "😐"
			if gay >= 50: m = "🔥"
			if gay >= 75: m = "🏳️‍🌈"
			await interaction.followup.send(f"<@{user.id}> is {gay}% gay {m}")
				
		registrate.fun.add_command(gayrate)
		
		@app_commands.command(name='gayrate_manipulate',description='copy of heist\'s gayrate')
		@app_commands.check(perms.is_owner)
		@app_commands.describe(user='gayrate user',gs='int')
		async def manipulate(interaction:Interaction,user:discord.User,gs:int):
			global CACHE
			CACHE[user.id]=gs
			await interaction.response.send(f"manipulated gs CACHE[{user.id}] = {gs}")
		