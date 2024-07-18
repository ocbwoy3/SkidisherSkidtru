#!/usr/bin/env python3

import os, traceback, sys, pathlib
os.chdir(__file__[:-8])

from api.dependency_check import dependency_check_auto
dependency_check_auto()

old_printfunc = print

def print(*args,namespace:str="SkidisherSkidtru",**kwargs):
	old_printfunc(f"\033[2;34m\033[1;34m[{namespace}]\033[0m\033[2;34m\033[0m",*args,**kwargs)

import dotenv
dotenv.load_dotenv()

import discord
from discord import app_commands, Interaction
from discord.app_commands import AppCommandError
import api.permissions as perms

from api.registrate import CommandRegistrate
from api.plugin import PluginLoader

bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

registrate = CommandRegistrate(tree,bot)
loader = PluginLoader(registrate)

from api.error_handler import setup_errorhandlers
setup_errorhandlers(tree)	

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.display_name} ({bot.user.name}#{bot.user.discriminator})")
	await bot.change_presence(status=discord.Status.idle,activity=discord.activity.Game("Skidisher Skidtru"))
	print("Loading plugins")
	loader.LoadPlugins()
	print("Finished loading plugins")
	print("Registering Command Groups from Registrate")
	tree.add_command(registrate.fun)
	tree.add_command(registrate.misc)
	tree.add_command(registrate.ocbwoy3)
	tree.add_command(registrate.mc)
	# tree.add_command(registrate.nexus)
	print("Syncing Command Tree")
	await tree.sync()
	print("Skidisher Skidtru has successfully loaded!")

def run_skidisherskidtru():
	# \033]8;;https://discord.gg/F8GwJBVVMU\033\\Discord Server\033]8;;\033\\
	old_printfunc(f"""
<r> ____  _    _     _ _     _               <x><y> ____  _    _     _ _              <x>
<r>/ ___|| | _(_) __| (_)___| |__   ___ _ __ <x><y>/ ___|| | _(_) __| | |_ _ __ _   _ <x>
<r>\___ \| |/ | |/ _` | / __| '_ \ / _ | '__|<x><y>\___ \| |/ | |/ _` | __| '__| | | |<x>
<r> ___) |   <| | (_| | \__ | | | |  __| |   <x><y> ___) |   <| | (_| | |_| |  | |_| |<x>
<r>|____/|_|\_|_|\__,_|_|___|_| |_|\___|_|   <x><y>|____/|_|\_|_|\__,_|\__|_|   \__,_|<x>

<b>Written by \033]8;;https://twitter.com/ocbwoy3\033\\OCbwoy3\033]8;;\033\\ and contributors<x>
""".replace('<r>','\x1B[1;31m').replace('<y>','\033[1;33m').replace('<x>','\033[0m').replace('<b>','\033[34m'))
	
	print('Skidisher Skidtru uses PrikolsHub\'s APIs and APIs of other services like SecLoad and Karma.')
	print('For more info, please run the about command.')
	
	import api.util as util

	util.check_terms()	
	
	import logging

	dform = logging.Formatter("\033[2;34m\033[1;34m[Discord]\033[0m\033[2;34m\033[0m {message}",style='{')

	print("Starting bot...")

	try:
		bot.run(os.getenv('DISCORD_TOKEN'),log_formatter=dform)
	except discord.errors.PrivilegedIntentsRequired:
		print("Skidisher Skidtru cannot access privileged intents required.")
		print("Please visit the Discord developer portal and enable privileged intents.")
	except discord.errors.LoginFailure as ex:
		print("Skidisher Skidtru was unable to log into Discord, this might have happened because you inputted an invalid token.")
		print(f"Exception: {ex}")
	except Exception as error:
		import traceback
		print("Skidisher Skidtru encountered an Exception.")
		traceback.print_exception(type(error), error, error.__traceback__,file=sys.stderr)

if __name__ == "__main__":
	run_skidisherskidtru()