#!/usr/bin/env python3

import dotenv, os, traceback, sys, pathlib
dotenv.load_dotenv()

old_printfunc = print

def print(*args,namespace:str="SkidisherSkidtru",**kwargs):
	old_printfunc(f"\033[2;34m\033[1;34m[{namespace}]\033[0m\033[2;34m\033[0m",*args,**kwargs)

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
	tree.add_command(registrate.fun)
	tree.add_command(registrate.misc)
	tree.add_command(registrate.ocbwoy3)
	tree.add_command(registrate.nexus)
	print("Syncing CommandTree")
	await tree.sync()
	print("Successfully loaded!")

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
	
	os.chdir(__file__[:-8])
	
	print('Skidisher Skidtru uses PrikolsHub\'s APIs and APIs of other services. For more info, please run the about command.')
	print("Loading Skidisher Skidtru")


	bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
	run_skidisherskidtru()