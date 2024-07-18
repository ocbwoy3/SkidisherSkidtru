import os, importlib, traceback, sys

import api.registrate as registrate

class PluginLoader:
	allPlugins = []
	def __init__(self,registrate:registrate.CommandRegistrate):
		self.registrate = registrate
		pass

	def load_extension(self,root_path:str,file_path:str):
		module_path = root_path+file_path
		module = importlib.import_module(module_path)

		def printfunc(*args,namespace:str=None,**kwargs):
			print(f"\033[2;34m\033[1;34m[{namespace or getattr(module,'__phmodn__')}]\033[0m\033[2;34m\033[0m",*args,**kwargs)

		setattr(module,"print",printfunc)
		setattr(module,"",print)
		setattr(module,"__registrate__",self.registrate)
		setattr(module,"__phmodn__",file_path)

		PluginName = getattr(module, "__plugin__",file_path)
		CreatorName = getattr(module, "__author__","Unknown")
		MainClass = getattr(module, "Main",None)

		if MainClass != None:
			self.allPlugins.append([module_path,PluginName,CreatorName])
			#print(f"\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m Loading \033[2;36m\033[1;36m{PluginName}\033[0m\033[2;36m\033[0m")
			MainClass(self.registrate)
			#print(f"\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m Successfully loaded \033[2;36m\033[1;36m{PluginName}\033[0m\033[2;36m\033[0m by \033[2;36m\033[1;36m{CreatorName}\033[0m\033[2;36m\033[0m")
		else:
			pass # print(f"\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m Skipped loading '{module_path}'")

	def LoadPlugins(self):
		for module_name in os.listdir("plugins/"):
			if module_name.endswith(".py") and ('__pychache__' not in module_name):
				module_path = f'plugins.{module_name[:-3]}'
				try:
					self.load_extension('plugins.',module_name[:-3])
				except Exception as error:
					print(f"\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m ({module_path}) {error.__class__.__name__}: {error}")
					print("".join(traceback.format_exception(type(error), error, error.__traceback__)),file=sys.stderr)

		# print("\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m Plugin Loading finished.")
		# print("\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m Currently loaded plugins:")
		# for plugin in self.allPlugins:
		# 	print(f"\033[2;34m\033[1;34m[Plugin]\033[0m\033[2;34m\033[0m {plugin[1]} by {plugin[2]} ({plugin[0]})")
