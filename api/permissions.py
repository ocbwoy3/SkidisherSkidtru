import discord, config

WHITELIST = config.WHITELIST

def is_ocbwoy3(interaction: discord.Interaction):
	if interaction.user.id == 486147449703104523:
		return True
	raise RuntimeError("ocbwoy3 only")

def is_whitelisted(interaction: discord.Interaction):
	if interaction.user.id == 486147449703104523:
		return True
	if interaction.user.id in WHITELIST:
		return True
	raise RuntimeError("wl only")