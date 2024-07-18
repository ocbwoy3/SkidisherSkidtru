from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

import api.permissions as perms

__plugin__ = "Skidisher Skidtru"
__author__ = "OCbwoy3"

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='about',description='Shows information about Skidisher Skidtru.')
		@app_commands.check(perms.is_whitelisted)
		async def SkidisherSkidtru_Command(interaction:Interaction,ephmereal:bool=True):
			if ephmereal != True:
				perms.is_whitelisted(interaction)
			await interaction.response.defer(ephemeral=ephmereal,thinking=True)
			await interaction.followup.send(f"""# Skidisher Skidtru
Written by OCbwoy3 and contributors.

Skidisher Skidtru is a super cool Discord user app written in Python, that anyone can self-host and use! It comes with a Plugin loader system for your custom plugin needs. Best of all, it's open source!

**Links**
> [GitHub]( <https://github.com/ocbwoy3/SkidisherSkidtru> )
> [Issues]( <https://github.com/ocbwoy3/SkidisherSkidtru/issues> )

**Acknowledgements**
> [Skidisher Skidtru]( <https://github.com/ocbwoy3/SkidisherSkidtru> ) - MIT
> [SecLoad]( <https://secload.scriptlang.com> ) - MIT
> [Karma]( <https://karma.doqe.dev> ) - Proprietary
> [PrikolsHub]( <https://discord.gg/F8GwJBVVMU> ) - Proprietary

**Open Source Licenses**
> [Python]( <https://github.com/python/cpython> ) - GPL
> [ro.py]( <https://github.com/ro-py/ro.py> ) - MIT
> [discord.py]( <https://github.com/Rapptz/discord.py> ) - MIT
> [uwuipy]( <https://github.com/Cuprum77/uwuipy> ) - MIT
> [requests]( <https://github.com/psf/requests> ) - Apache 2.0
> [cfscrape]( <https://github.com/Anorov/cloudflare-scrape> ) - MIT
> [pylast]( <https://github.com/pylast/pylast> ) - Apache 2.0
> [groq]( <https://github.com/groq/groq-python> ) - Apache 2.0""",ephemeral=ephmereal)
				
		registrate.misc.add_command(SkidisherSkidtru_Command)
