import discord
from discord import app_commands, AppCommandContext, AppInstallationType

class CommandRegistrate:
	def __init__(self,tree:app_commands.CommandTree,bot:discord.Client):
		self.tree = tree
		self.bot = bot

	fun = app_commands.Group(name='fun',description='Fun Commands',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())
	misc = app_commands.Group(name='misc',description='Extra Commands',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())
	ocbwoy3 = app_commands.Group(name='ocbwoy3',description='Spy on OCbwoy3',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())
	nexus = app_commands.Group(name='nexus',description='Nexus lookup commands',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())
	prikolshub = app_commands.Group(name='prikolshub',description='Fun',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())

	