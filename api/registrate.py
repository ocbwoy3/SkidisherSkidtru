import discord
from discord import app_commands, AppCommandContext, AppInstallationType

class CommandRegistrate:
	fun = app_commands.Group(name='fun',description='Fun Commands',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())
	misc = app_commands.Group(name='misc',description='Extra Commands',allowed_contexts=AppCommandContext.all(),allowed_installs=AppInstallationType.all())