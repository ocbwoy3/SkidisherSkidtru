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

import cfscrape, functools, asyncio
from requests import Response

async def cfget(*args, **kwargs) -> Response:
	scraper = cfscrape.create_scraper()
	realfunc = functools.partial(scraper.get, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	return response

async def cfpost(*args, **kwargs) -> Response:
	scraper = cfscrape.create_scraper()
	realfunc = functools.partial(scraper.post, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	return response

async def delete(*args, **kwargs) -> Response:
	scraper = cfscrape.create_scraper()
	realfunc = functools.partial(scraper.delete, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	return response

SCRIPT_EXP = 5

async def getSecloadScript(username:str, exp:int=SCRIPT_EXP):
	scriptupload = {
		"Key": conf.SECLOAD_API_KEY,
		"ScriptName": "prikolshub",
		"Username": username,
		"Time": SCRIPT_EXP
	}
	jd = json.dumps(scriptupload)
	d = await cfpost("https://secload.scriptlang.com/secload/publicapi/GenerateKey",data=jd)
	d.raise_for_status()
	return d.text

class Main:
	def __init__(self, registrate:CommandRegistrate):
		if conf.SECLOAD_API_KEY != "EXAMPLE.KEY":

			@app_commands.command(name="script",description="Generates the script using SecLoad.")
			@app_commands.describe(username="Roblox Username of the person running the script.",raw="Disable formatting as lua, useful for mobile users.",ephemeral="Define if the message should be ephemeral, default: true",expire="Define in how many minutes the script should expire.")
			@app_commands.check(perms.is_whitelisted)
			@app_commands.checks.cooldown(1,15)
			async def generateScriptCommand_owner(interaction: Interaction, username:str, expire:int=SCRIPT_EXP, raw:bool=False, ephemeral:bool=True):
				await interaction.response.defer(ephemeral=ephemeral,thinking=True)
				try:
					scr = await getSecloadScript(username[:20],exp=expire)
					print(f"{interaction.user.name}#{interaction.user.discriminator} generated script - {scr}")
					if raw == True:
						await interaction.followup.send(f"{scr}",ephemeral=ephemeral)
					else:
						await interaction.followup.send(f'```lua\n{scr}\n```',ephemeral=ephemeral)
				except Exception as ex:
					await interaction.followup.send(f"(This might be an error with cfscrape, the SecLoad API or something else.)\n{ex.__class__.__name__}: {ex}",ephemeral=ephemeral)

			registrate.prikolshub.add_command(generateScriptCommand_owner)
		
		else:
			print("The SecLoad integration is disabled! Make sure you defined SECLOAD_API_KEY in the config.py!")
			print("Refer to SecLoad API docs at https://secload.scriptlang.com/docs/")