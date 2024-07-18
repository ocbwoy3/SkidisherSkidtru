from api.registrate import CommandRegistrate
from discord import app_commands, Interaction

import discord, typing
import config as conf
import json
from discord.ext import tasks

import api.permissions as perms

__plugin__ = "SecLoad"
__author__ = "OCbwoy3"

# ez cloudflare bypass

import functools, asyncio
from requests import Response

SCRIPT_EXP = 5

import typing
from api.SecLoad import SecLoad

class Main:
	def __init__(self, registrate:CommandRegistrate):
		if conf.SECLOAD_API_KEY != "":

			sl = SecLoad(conf.SECLOAD_API_KEY)
			script = sl.GetScript("prikolshub")

			global scripts
			scripts = []

			global autofill
			autofill = []

			async def fetchScripts():
				global scripts, autofill
				scripts = await sl.GetScripts()
				autofill = [
					discord.app_commands.Choice(name=script.name,value=script.name) for script in scripts
				]
				print("Fetched scripts!",scripts,autofill)

			import asyncio
			@tasks.loop(seconds=1,count=1)
			async def lol():
				try:
					await fetchScripts()
				except Exception as ex:
					print(f"Script fetch error: f{ex}")

			lol.start()

			async def scriptAutocomplete(interaction:Interaction,current:str) -> typing.List[discord.app_commands.Choice[str]]:
				retval = [
					choice for choice in autofill if current.lower() in choice.name.lower()
				]
				return retval[:25]

			@app_commands.command(name="refetch",description="Refetches the SecLoad scripts.")
			@app_commands.check(perms.is_ocbwoy3)
			@app_commands.checks.cooldown(1,15)
			async def refetchScriptsCommand(interaction: Interaction):
				await interaction.response.defer(ephemeral=True,thinking=True)
				await fetchScripts()
				await interaction.followup.send("Success",ephemeral=True)

			registrate.misc.add_command(refetchScriptsCommand)

			@app_commands.command(name="generate",description="Generate a script using SecLoad.")
			@app_commands.describe(script="The script's name.",username="Roblox Username of the person running the script.",raw="Disable formatting as lua, useful for mobile users.",ephemeral="Define if the message should be ephemeral, default: true",expire="Define in how many minutes the script should expire.")
			@app_commands.check(perms.is_whitelisted)
			@app_commands.autocomplete(script=scriptAutocomplete)
			@app_commands.checks.cooldown(1,15)
			async def generateScriptCommand(interaction: Interaction, script:str, username:str, expire:int=SCRIPT_EXP, raw:bool=False, ephemeral:bool=True):
				await interaction.response.defer(ephemeral=ephemeral,thinking=True)
				scrip = sl.GetScript(script)
				scr = await scrip.GenerateRequire(username,time=expire)
				print(f"{interaction.user.name}#{interaction.user.discriminator} generated script - {scr}")
				if raw == True:
					await interaction.followup.send(f"{scr}",ephemeral=ephemeral)
				else:
					await interaction.followup.send(f'```lua\n{scr}\n```',ephemeral=ephemeral)

			registrate.misc.add_command(generateScriptCommand)

			@app_commands.command(name="delete",description="Generate a SecLoad script.")
			@app_commands.describe(script="The script's name.")
			@app_commands.check(perms.is_ocbwoy3)
			@app_commands.autocomplete(script=scriptAutocomplete)
			@app_commands.checks.cooldown(1,15)
			async def deleteScriptCommand(interaction: Interaction, script:str):
				await interaction.response.defer(ephemeral=True,thinking=True)
				scrip = sl.GetScript(script)
				await scrip.Delete()
				await fetchScripts()
				await interaction.followup.send(f'Success',ephemeral=True)

			registrate.misc.add_command(deleteScriptCommand)

			@app_commands.command(name="upload",description="Upload a script to SecLoad.")
			@app_commands.describe(script="The script's name.",source="The source file for the script.")
			@app_commands.check(perms.is_ocbwoy3)
			@app_commands.checks.cooldown(1,15)
			async def uploadScriptCommand(interaction: Interaction, script:str, source:discord.Attachment):
				await interaction.response.defer(ephemeral=True,thinking=True)
				await sl.CreateScript(script,str(source.read()))
				await fetchScripts()
				await interaction.followup.send(f'Success',ephemeral=True)

			registrate.misc.add_command(uploadScriptCommand)

			@app_commands.command(name="overwrite",description="Overwrite a SecLoad script.")
			@app_commands.describe(script="The script's name.",source="The source file for the script.")
			@app_commands.autocomplete(script=scriptAutocomplete)
			@app_commands.check(perms.is_ocbwoy3)
			@app_commands.checks.cooldown(1,15)
			async def updateScriptCommand(interaction: Interaction, script:str, source:discord.Attachment):
				await interaction.response.defer(ephemeral=True,thinking=True)
				scrip = sl.GetScript(script)
				await scrip.UpdateSource(str(source.read()))
				await fetchScripts()
				await interaction.followup.send(f'Success',ephemeral=True)

			registrate.misc.add_command(updateScriptCommand)

		else:
			print("The SecLoad integration is disabled! Make sure you defined SECLOAD_API_KEY in the config.py!")
			print("Refer to SecLoad API docs at https://secload.scriptlang.com/docs/")