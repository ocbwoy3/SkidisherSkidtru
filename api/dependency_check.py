import sys, os, importlib

old_printfunc = print

def print(*args,namespace:str="DependencyCheck",**kwargs):
	old_printfunc(f"\033[2;34m\033[1;34m[{namespace}]\033[0m\033[2;34m\033[0m",*args,**kwargs)

def install_package_if_not_present(package_name:str,import_name:str=None):
	"""
	Installs a package using pip, if not present.
	"""
	try:
		importlib.import_module(import_name or package_name)
		print(f"Package {package_name} present.")
		return True
	except:
		print(f"Package {package_name} not present, installing.")
		print(f"Executing shell command: {sys.executable} -m pip install {package_name}")
		os.system(f"{sys.executable} -m pip install {package_name}")
	try:
		importlib.import_module(import_name or package_name)
		print(f"Successfully installed {package_name}")
		return True
	except:
		print("Failed to import module after install.")
		exit(1)


def dependency_check_auto():
	"""
	Main function for Skidisher Skidtru to check dependencies.
	"""

	install_package_if_not_present("discord","discord") # discord.py PR #9760 got merged 
	install_package_if_not_present("python-dotenv","dotenv")
	install_package_if_not_present("cfscrape")
	install_package_if_not_present("distro")
	install_package_if_not_present("roblox")
	install_package_if_not_present("uwuipy")
	install_package_if_not_present("requests")
	install_package_if_not_present("pylast")