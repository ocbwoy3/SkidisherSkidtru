#!/usr/bin/env python3

import dotenv, os, traceback, sys
dotenv.load_dotenv()

import discord
from discord import app_commands, Interaction
from discord.app_commands import AppCommandError

from api.registrate import CommandRegistrate
from api.plugin import PluginLoader

bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

registrate = CommandRegistrate()
loader = PluginLoader(registrate)

@tree.error
async def on_tree_error(interaction: Interaction, error: AppCommandError) -> None:
	if isinstance(error, app_commands.CheckFailure):
		try:
			await interaction.response.send_message("You are not allowed to access this command!",ephemeral=True)
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
	print("[SkidisherSkidtru]",f"Logged in as {bot.user.display_name} ({bot.user.name}#{bot.user.discriminator})")
	await bot.change_presence(status=discord.Status.idle)
	loader.LoadPlugins()
	tree.add_command(registrate.fun)
	tree.add_command(registrate.misc)
	await tree.sync()
	print("[SkidisherSkidtru]","Successfully synced CommandTree.")

if __name__ == "__main__":
	bot.run(os.getenv('DISCORD_TOKEN'))