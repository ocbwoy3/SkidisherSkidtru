import sys, os

TERM_ACCEPT_FILENAME = ".skidisherskidtru-accept-terms"
old_printfunc = print

def print(*args,namespace:str="SkidisherSkidtru",**kwargs):
	old_printfunc(f"\033[2;34m\033[1;34m[{namespace}]\033[0m\033[2;34m\033[0m",*args,**kwargs)

def ask_for_terms():
	print("Acceptance of terms is required in order to continue.")
	old_printfunc(f"""
Nexus's, SecLoad's and PrikolsHub's APIs use is governed by their respective terms.
Abuse of API might result in your IP address being blacklisted, which might limit the functionality of Skidisher Skidtru.

Here is a summarized list of API policies. May not be full version and such, but you get the point.

Nexus:
	Do not spam requests
	Do not use Roblox-Only endpoints at all

SecLoad:
	Do not spam requests
	Do not upload scripts that break Roblox's community standards and terms of use

PrikolsHub:
	Do not spam requests
	Do not abuse the API to make session requests
	Do not use library, session and session request endpoints
""")
	try:
		res = input("Do you accept these terms? [y/N]: ").lower()
		if res[0:1] == 'y':
			return True
		else:
			return False
	except:
		return False
	
def check_terms():
	try:
		if os.path.isfile(TERM_ACCEPT_FILENAME) == True:
			return True
	except:
		pass
	accepted = ask_for_terms()
	if accepted == True:
		try:
			with open(TERM_ACCEPT_FILENAME,'w') as file:
				file.write('True')
				file.close()
				print("Terms were accepted")
		except Exception as ex:
			print(f"Failed to write to term acceptance file. {ex}")
			exit(1)
	else:
		print("Terms were declined, exiting.")
		exit(0)