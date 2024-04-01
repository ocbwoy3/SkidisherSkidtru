from api.registrate import CommandRegistrate
import discord
from discord import app_commands, Interaction

from api.view import BaseView
import api.permissions as perms

import uuid

__plugin__ = "Global Bans"
__author__ = "OCbwoy3"

import functools, requests, asyncio
from requests import Response

import cfscrape

async def get(*args, **kwargs) -> Response:
	scraper = cfscrape.create_scraper()
	realfunc = functools.partial(scraper.get, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	return response

async def post(*args, **kwargs) -> Response:
	scraper = cfscrape.create_scraper()
	realfunc = functools.partial(scraper.post, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	return response


import roblox
client = roblox.Client()

class Main:
	def __init__(self,registrate:CommandRegistrate):

		@app_commands.command(name='ban_check',description='Check if a user is banned using 112, Nexus and Doqium.')
		@app_commands.describe(player='Username of the player you want to match bans against.',ephmereal='Shows the message only for you')
		@app_commands.check(perms.is_whitelisted)
		async def ban_check(interaction:Interaction,player:str,ephmereal:bool=False):
			await interaction.response.defer(ephemeral=ephmereal,thinking=True)

			user = await client.get_user_by_username(username=player,exclude_banned_users=False)

			view = BaseView(user=None,timeout=None)

			link = discord.ui.Button[BaseView](label="View User",style=discord.ButtonStyle.link,url=f"https://roblox.com/users/{user.id}")
			view.add_item(link)

			b_112 = (await get("https://lietuva.scriptlang.com/banland.json")).json()
			b_nexus = (await get("https://nexus.scriptlang.com/bans")).json()

			embed = discord.Embed(colour=discord.Colour.green(),title=f"{user.display_name or user.name} (@{user.name})",description="",url=f"https://roblox.com/users/{user.id}")

			isBanned = False
			if b_112.get(f'{user.id}',None) != None:
				isBanned = True
				embed.add_field(name="112 (PrikolsHub):",value = b_112.get(f'{user.id}','skidisher skidtru dummy ban reason'))
			if b_nexus.get(f'{user.id}',None) != None:
				isBanned = True
				embed.add_field(name="Nexus:",value = b_nexus.get(f'{user.id}').get('reason','skidisher skidtru dummy ban reason'))
				link2 = discord.ui.Button[BaseView](label="View on Nexus Bans",style=discord.ButtonStyle.link,url=f"https://nexusbans.scriptlang.com")
				view.add_item(link2)


			if isBanned == False:
				embed.description = 'This user is not banned.'

			view.message = await interaction.followup.send(view=view,embed=embed)

		registrate.misc.add_command(ban_check)

		@app_commands.command(name='lookup',description='Perform a username lookup on Nexus\'s whitelist and blacklist.')
		@app_commands.describe(player='Username of the player you want to look up.',ephmereal='Shows the message only for you')
		@app_commands.check(perms.is_whitelisted)
		async def nexus_db_lookup(interaction:Interaction,player:str,ephmereal:bool=False):
			await interaction.response.defer(ephemeral=ephmereal,thinking=True)

			user = await client.get_user_by_username(username=player,exclude_banned_users=False)

			view = BaseView(user=None,timeout=None)

			link = discord.ui.Button[BaseView](label="View User",style=discord.ButtonStyle.link,url=f"https://roblox.com/users/{user.id}")
			view.add_item(link)

			b_wl = (await get("https://nexus.scriptlang.com/whitelist")).json()
			b_bl = (await get("https://nexus.scriptlang.com/bans")).json()

			embed = discord.Embed(colour=discord.Colour.green(),title=f"{user.display_name or user.name} (@{user.name})",description="",url=f"https://roblox.com/users/{user.id}")

			if b_wl.get(f'{user.id}',None) != None:
				o = b_wl.get(f'{user.id}')
				embed.add_field(name="Linked discord:",value = f"<@{o.get('discord','1')}>",inline=False)
				
			if b_bl.get(f'{user.id}',None) != None:
				embed.add_field(name="Banned for:",value = b_bl.get(f'{user.id}').get('reason','skidisher skidtru dummy ban reason'),inline=False)

			if len(embed.fields) == 0:
				embed.description = "Could not find any information when looking up the user."

			view.message = await interaction.followup.send(view=view,embed=embed)

		registrate.nexus.add_command(nexus_db_lookup)

		@app_commands.command(name='whois',description='Perform a reverse lookup on Nexus\' whitelist.')
		@app_commands.describe(user='User to perform a reverse lookup on.',ephmereal='Shows the message only for you')
		@app_commands.check(perms.is_whitelisted)
		async def reverse_nexus_db_lookup(interaction:Interaction,user:discord.User,ephmereal:bool=False):
			await interaction.response.defer(ephemeral=ephmereal,thinking=True)

			view = BaseView(user=None,timeout=None)

			b_wl = (await get("https://nexus.scriptlang.com/whitelist")).json()

			embed = discord.Embed(colour=discord.Colour.green(),title=f"{user.display_name}",description="",url=f"https://roblox.com/users/{user.id}")

			for i in b_wl.keys():
				try:
					e = b_wl.get(i)
					if e.get('discord',1) == user.id:
						embed.add_field(name=e.get('plr'),value=f'{str(i)}',inline=False)
				except:
					pass

			if len(embed.fields) == 0:
				embed.description = "User has no linked accounts in Nexus's whitelist."

			view.message = await interaction.followup.send(view=view,embed=embed)

		registrate.nexus.add_command(reverse_nexus_db_lookup)