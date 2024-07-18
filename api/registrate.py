import discord
from discord import app_commands
from discord.app_commands.installs import AppCommandContext, AppInstallationType

ct = AppCommandContext(guild=True,dm_channel=True,private_channel=True)
ins = AppInstallationType(guild=True,user=True)

class CommandRegistrate:
	def __init__(self,tree:app_commands.CommandTree,bot:discord.Client):
		self.tree = tree
		self.bot = bot

	fun = app_commands.Group(name='fun',description='Fun Commands',allowed_contexts=ct,allowed_installs=ins)
	misc = app_commands.Group(name='misc',description='Extra Commands',allowed_contexts=ct,allowed_installs=ins)
	ocbwoy3 = app_commands.Group(name='ocbwoy3',description='Spy on OCbwoy3',allowed_contexts=ct,allowed_installs=ins)
	prikolshub = app_commands.Group(name='prikolshub',description='Fun',allowed_contexts=ct,allowed_installs=ins)
	mc = app_commands.Group(name='mc',description='Manage a Minecraft Server',allowed_contexts=ct,allowed_installs=ins)

