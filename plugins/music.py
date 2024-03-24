from api.registrate import CommandRegistrate
import discord, pylast, os
from discord import app_commands, Interaction

from api.view import BaseView
import api.permissions as perms

__plugin__ = "Music Status"
__author__ = "OCbwoy3"

class Main:
	def __init__(self,registrate:CommandRegistrate):

		network = pylast.LastFMNetwork(
			api_key=os.getenv("LASTFM_API_KEY"),
			api_secret=os.getenv("LASTFM_SHARED_SECRET"),
			username=os.getenv("LASTFM_USERNAME"),
			password_hash=pylast.md5(os.getenv("LASTFM_PASSWORD"))
		)
		authed = network.get_authenticated_user()

		print(f"Logged in as {authed.get_name()}",namespace="LastFM")

		@app_commands.command(name='music',description='Shows the current status of music being listened to by OCbwoy3.')
		@app_commands.check(perms.is_whitelisted)
		@app_commands.checks.cooldown(1,15)
		async def get_music(interaction:Interaction):
			await interaction.response.defer(ephemeral=False,thinking=True)

			nowplaying = authed.get_now_playing()

			if nowplaying == None:
				await interaction.followup.send("No music currently playing.")
				return

			link = nowplaying.get_url()
			artwork = nowplaying.get_cover_image(pylast.SIZE_MEDIUM)
			title = nowplaying.get_title(properly_capitalized=True)
			artist = nowplaying.get_artist().get_name()
			album = nowplaying.get_album().get_name()

			embed = discord.Embed(color=discord.Colour.red(),title=f"{title}",url=link)
			embed.add_field(name="Title",value=f"{title}",inline=False)
			embed.add_field(name="Artist",value=f"{artist}",inline=False)
			embed.add_field(name="Album",value=f"{album}",inline=False)
			embed.set_footer(text="Music API data from last.fm")
			embed.set_thumbnail(url=artwork)

			view = BaseView(user=None,timeout=None)
			link = discord.ui.Button[BaseView](label="View on last.fm",style=discord.ButtonStyle.link,url=f"{link or 'https://google.com/search?q=error'}")
			view.add_item(link)

			await interaction.followup.send(embed=embed,view=view)
				
		registrate.ocbwoy3.add_command(get_music)