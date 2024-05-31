"""
SecLoad API implementation for Skidisher Skidtru.
"""

import requests_html, functools, asyncio
from requests import Response

from .exceptions import *

import json

ROOT_URL = "https://secload.ocbwoy3.dev"

P_APIRoot = ROOT_URL + "/secload/publicapi"

async def cfget(*args, **kwargs) -> Response:
	"""
	Async function to get data with Cloudflare bypass.
	"""
	# print(args,kwargs)
	scraper = requests_html.HTMLSession() # cfscrape.create_scraper()
	realfunc = functools.partial(scraper.get, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	# print(response.text)
	return response

async def cfpost(*args, **kwargs) -> Response:
	"""
	Async function to post data with Cloudflare bypass.
	"""
	# print(args,kwargs)
	scraper = requests_html.HTMLSession() # cfscrape.create_scraper()
	realfunc = functools.partial(scraper.post, *args, **kwargs)
	loop = asyncio.get_running_loop()
	response = await loop.run_in_executor(None,realfunc)
	# print(response.text)
	return response

async def GenerateKey(length:int=50) -> str:
	"""
	Generates a new SecLoad API key with the given length.
	"""
	if length < 30:
		raise KeyGenerationException("The key's length must be equal to, or greater than 30.")
	
	dat = await cfpost(P_APIRoot+"/GenerateAPIKey",data=json.dumps({
		"Length": length
	}))
	dat.raise_for_status()

	return str(dat.text)

class Script:
	"""
	Represents a SecLoad script.
	"""
	__apikey__: str
	name: str

	def __repr__(self): return f"<SecLoad script \"{self.name}\">"
	def __str__(self): return f"Script(\"{self.name}\")"
	

	def __init__(self,api_key:str,script:str):
		"""
		Initalizes the script object with the API key and the script's name.
		"""
		self.__apikey__ = api_key
		self.name = script

	async def GetSource(self) -> str:
		"""
		Gets the script's source and returns it as a string.
		"""
		d = await cfpost(P_APIRoot+"/GetScriptSource",data=json.dumps({
			"Key": self.__apikey__,
			"ScriptName": self.name,
			"Type": "text"
		}))

		if d.text == "API key does not exist":
			raise AuthException("Invalid API key.")
		
		if d.text == "Script does not exist":
			raise ScriptDoesntExist(f"Script \"{self.name}\" doesn't exist.")
		
		if d.text == "API script list exceeds 5,000,000 Bytes (5 Megabytes)":
			raise SizeException("Scripts exceed 5MB limit.")

		d.raise_for_status()
		return d.text
	
	async def GenerateRequire(self,username:str,time:int=5) -> str:
		"""
		Generates a require for the given script.
		If `time` is `0`, then the script's key will last forever, and can be executed more than once.
		"""

		if len(username) > 20:
			InvalidUsername("Roblox Usernames have a maximum length of 20 chars.")

		d = await cfpost(P_APIRoot+"/GenerateKey",data=json.dumps({
			"Key": self.__apikey__,
			"ScriptName": self.name,
			"Username": username[:20],
			"Time": time
		}))

		if d.text == "API key does not exist":
			raise AuthException("Invalid API key.")
		
		if d.text == "Script does not exist":
			raise ScriptDoesntExist(f"Script \"{self.name}\" doesn't exist.")
		
		if d.text == "API script list exceeds 5,000,000 Bytes (5 Megabytes)":
			raise SizeException("Scripts exceed 5MB limit.")

		d.raise_for_status()
		return d.text

	async def UpdateSource(self,new_source:str):
		"""
		Generates a require for the given script.
		If `time` is `0`, then the script's key will last forever, and can be executed more than once.
		"""

		d = await cfpost(P_APIRoot+"/OverwriteScript",data=json.dumps({
			"Key": self.__apikey__,
			"ScriptName": self.name,
			"Source": new_source
		}))

		d.raise_for_status()

		if d.text == "API key does not exist":
			raise AuthException("Invalid API key.")
		
		if d.text == "Script does not exist":
			raise ScriptDoesntExist(f"Script \"{self.name}\" doesn't exist.")
		
		if d.text == "API script list exceeds 5,000,000 Bytes (5 Megabytes)":
			raise SizeException("Scripts exceed 5MB limit.")

		if d.text != "\"Success\"":
			raise Exception(f"Invalid response: {d.text}")

		
	async def Delete(self):
		"""
		Removes the Script from SecLoad.
		"""

		d = await cfpost(P_APIRoot+"/RemoveScript",data=json.dumps({
			"Key": self.__apikey__,
			"ScriptName": self.name
		}))

		if d.text == "API key does not exist":
			raise AuthException("Invalid API key.")
		
		if d.text == "Script does not exist":
			raise ScriptDoesntExist(f"Script \"{self.name}\" doesn't exist.")
		
		if d.text == "API script list exceeds 5,000,000 Bytes (5 Megabytes)":
			raise SizeException("Scripts exceed 5MB limit.")
		
		d.raise_for_status()

		if d.text != "\"Success\"":
			raise Exception(f"Invalid response: {d.text}")

class SecLoad:
	"""
	Represents the SecLoad API.
	"""
	__apikey__: str

	def __repr__(self): return f"<SecLoad>"
	def __str__(self): return f"SecLoad()"

	def __init__(self,api_key:str):
		"""
		Connects to the SecLoad API with the given `api_key`.
		"""
		self.__apikey__ = api_key

	async def GetScripts(self) -> list[Script]:
		"""
		Get a list of scrips.
		"""
		
		d = await cfpost(P_APIRoot+"/ListScripts",data=json.dumps({
			"Key": self.__apikey__
		}))

		if d.text == "API key does not exist":
			raise AuthException("Invalid API key.")
		
		if d.text == "Script does not exist":
			raise ScriptDoesntExist(f"Script \"{self.name}\" doesn't exist.")
		
		if d.text == "API script list exceeds 5,000,000 Bytes (5 Megabytes)":
			raise SizeException("Scripts exceed 5MB limit.")
		
		d.raise_for_status()
		sl = d.json()

		return [
			Script(self.__apikey__,name) for name in sl
		]
	
	async def CreateScript(self,name:str,source:str) -> Script:
		"""
		Create a script.
		"""
		
		d = await cfpost(P_APIRoot+"/CreateScript",data=json.dumps({
			"Key": self.__apikey__,
			"ScriptName": name,
			"Source": source
		}))


		if d.text == "API key does not exist":
			raise AuthException("Invalid API key.")
		
		if d.text == "Script does not exist":
			raise ScriptDoesntExist(f"Script \"{self.name}\" doesn't exist.")
		
		if d.text == "API script list exceeds 5,000,000 Bytes (5 Megabytes)":
			raise SizeException("Scripts exceed 5MB limit.")
		
		d.raise_for_status()
		sl = d.json()

		return Script(self.__apikey__,name)

	def GetScript(self,script_name:str) -> Script:
		"""
		Returns a script with the provided name.
		"""
		return Script(self.__apikey__,script_name)