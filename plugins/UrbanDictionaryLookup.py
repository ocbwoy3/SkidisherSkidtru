from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

from api.view import BaseView
import api.permissions as perms

import functools, cfscrape, asyncio
from requests import Response

async def cfget(*args, **kwargs) -> Response:
	scraper = cfscrape.create_scraper()
	realfunc = functools.partial(scraper.get, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	return response

import re
import dateutil.parser as dparse
import urllib.parse as parse

__plugin__ = "Urban Dictionary"
__author__ = "OCbwoy3"

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='urban',description='Let Skidisher Skidtru define a term using the Urban Dictionary.')
		@app_commands.describe(term="The term to define.",ephemeral="Define if the message should be ephemeral, default: false")
		async def define_term(interaction:Interaction,term:str,ephemeral:bool=False):
			await interaction.response.defer(ephemeral=ephemeral,thinking=True)
			
			query = f"https://api.urbandictionary.com/v0/define?term={ parse.quote(term[:50]) }&per_page=10"
			#print("SkidisherSkidtru urban command debug:",query)
			query2 = parse.quote(term.strip())
			definitions = (await cfget(query)).json().get('list',[])

			if len(definitions) == 0:
				await interaction.followup.send("No results found.")

			def reduce_func(x,y):
				if x.get('thumbs_up') > y.get('thumbs_up'):
					return x
				else:
					return y
			
			if len(definitions) == 1:
				definiton = definitions[0]
			else:
				definition = functools.reduce(reduce_func,definitions)
			desc: str = definition.get('definition')

			def linkify(text:str) -> str:
				tx = text.replace('\r\n','\n')
				tx = re.sub(pattern=r"([\*\>\_`~\\])*",repl=r"",string=tx)
				tx = re.sub(pattern=r"\[(.+?)\]",string=tx,repl=lambda word:
					(word.group() is not None) and
					f"{str(word.group())}(https://www.urbandictionary.com/define.php?term={ parse.quote(str(word.group())[1:-1]) } \"Define '{str(word.group())[1:-1]}' on Urban Dictionary\")"
					or "")
				return tx.strip()

			view = BaseView(user=None,timeout=None)

			link = discord.ui.Button[BaseView](label="View on Urban Dictionary",style=discord.ButtonStyle.link,url=f"https://www.urbandictionary.com/define.php?term={query2}")
			view.add_item(link)

			embed = discord.Embed(title=f"{definition.get('word')}",description="",url=f"https://www.urbandictionary.com/define.php?term={query2}")
			embed.set_author(name=f"Uploaded by {definition.get('author')}",url=f"https://www.urbandictionary.com/author.php?author={ parse.quote(definition.get('author')) }")
			embed.description = linkify(desc)
			embed.add_field(name="Example",value=linkify(definition.get('example')),inline=False)
			embed.add_field(name="Want more definitions?",value=f"Check out [more definitions](https://www.urbandictionary.com/define.php?term={query2} \"Define '{term.strip()}' on Urban Dictionary\") on Urban Dictionary.",inline=False)
			embed.colour = discord.Colour(0xFF9900)
			embed.set_footer(text=f"👍 {str(definition.get('thumbs_up'))} | 👎 {str(definition.get('thumbs_down'))}")
			embed.timestamp = dparse.parse(definition.get('written_on'))

			view.message = await interaction.followup.send(view=view,embed=embed)

		registrate.fun.add_command(define_term)