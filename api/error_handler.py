import discord, os, sys, traceback
from discord import Interaction, app_commands
from discord.app_commands import AppCommandError, CommandTree

def setup_errorhandlers(tree: CommandTree):
	@tree.error
	async def on_tree_error(interaction: Interaction, error: AppCommandError) -> None:
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
			check_failture = isinstance(error, app_commands.CheckFailure)
			tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
			print(f'Ignoring exception in command {interaction.command.name}:\n{tb}', file=sys.stderr)
			import platform
			windows_version = sys.getwindowsversion()
			m2 = f"""**Skidisher Skidtru**
{
	sys.platform == "win32" and
	f"> OS: Windows {windows_version.major}.{windows_version.minor} (OS Build {windows_version.build})"
	or f"> OS: {platform.system()} {platform.release()}"
}
> OS platform: {sys.platform}
> Python {platform.python_version()} ({platform.python_implementation()})
> Working Directory: `{os.getcwd()}`
> Python Executable: `{sys.executable}`
> Current file: `{__file__}`
> Process PID: {os.getpid()}"""
			message = f"""# Skidisher Skidtru has encountered an Exception.
If this occours again, please create an [issue](<https://github.com/ocbwoy3/SkidisherSkidtru/issues>).
{
	check_failture == True and
	':warning: This is a Check Failture, most likely intentional, or undocumented.' or ''
}
**Slash Command Interaction**
> ID: {interaction.id}
> User: {interaction.user.id}
> Channel: {interaction.channel_id} (<#{interaction.channel_id}>)
> Guild: {interaction.guild_id}
> Command: {interaction.command.name}
> Error Message: `{error}`"""
			print(message+f"\n\n{m2}")
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			try:
				await interaction.response.send_message(message+f"\n\n{m2}",ephemeral=True)
				await interaction.followup.send(f"""## Stack trace\n```py\n{tb}\n```""",ephemeral=True)
			except Exception as ex:
				try:
					await interaction.followup.send(message+f"\n\n{m2}",ephemeral=True)
					await interaction.followup.send(f"""## Stack trace\n```py\n{tb}\n```""",ephemeral=True)
				except Exception as ex2:
					print(ex,ex2)