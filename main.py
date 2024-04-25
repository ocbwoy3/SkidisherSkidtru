#!/usr/bin/env python3

import dotenv, os, traceback, sys
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

@tree.error
async def on_tree_error(interaction: Interaction, error: AppCommandError) -> None:
	#if isinstance(error, app_commands.CheckFailure):
	#	try:
	#		await interaction.response.send_message("Unable to run this command.",ephemeral=True)
	#	except:
	#		pass
	#	return
	if isinstance(error, app_commands.CommandOnCooldown):
		try:
			await interaction.response.send_message(str(error),ephemeral=True)
		except Exception as ex:
			try:
				await interaction.followup.send(str(error),ephemeral=True)
			except:
				pass
		return
	elif 'ocbwoy3 only' in str(error):
		try:
			await interaction.response.send_message("You are not OCbwoy3!",ephemeral=True)
		except Exception as ex:
			try:
				await interaction.followup.send("You are not OCbwoy3!",ephemeral=True)
			except:
				pass
		return
	elif 'wl only' in str(error):
		try:
			await interaction.response.send_message("You are not whitelisted!",ephemeral=True)
		except Exception as ex:
			try:
				await interaction.followup.send("You are not whitelisted!",ephemeral=True)
			except:
				pass
		return
	else:
		print(f'Ignoring exception in command {interaction.command.name}:', file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
		message = f"An error occurred while processing the slash command interaction for '{str(interaction.command.name)}':\n```py\n{tb}\n```"
		try:
			await interaction.response.send_message(message,ephemeral=True)
		except Exception as ex:
			try:
				await interaction.followup.send(message,ephemeral=True)
			except:
				pass

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

if __name__ == "__main__":
	bot.run(os.getenv('DISCORD_TOKEN'))