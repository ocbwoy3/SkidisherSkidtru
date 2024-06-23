import sys, os

TERM_ACCEPT_FILENAME = ".skidisherskidtru_accept_terms"
old_printfunc = print

def print(*args,namespace:str="SkidisherSkidtru",**kwargs):
	old_printfunc(f"\033[2;34m\033[1;34m[{namespace}]\033[0m\033[2;34m\033[0m",*args,**kwargs)

def ask_for_terms():
	print("Acceptance of terms is required in order to continue.")
	old_printfunc(f"""
Usage of Karma's, SecLoad's and PrikolsHub's APIs are governed by their respective terms.
Abuse of API might result in your IP address being blacklisted, which might limit the functionality of Skidisher Skidtru.

You get the point.

Karma:
	Do not spam requests
	Do not use Roblox-Only endpoints at all (Instant Ban)
	Proxies and VPNs are banned

SecLoad:
	Do not spam requests
	Do not upload scripts that break Roblox's community standards and terms of use

PrikolsHub:
	Do not spam requests
	Do not abuse the API to make session requests
	Do not use library, session and session request endpoints
""")
	try:
		res = input("Do you agree to these terms? [y/N]: ").lower()
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
		print(f"Writing to file: {TERM_ACCEPT_FILENAME}")
		try:
			with open(TERM_ACCEPT_FILENAME,'w') as file:
				file.write('True')
				file.close()
				print("Success!")
		except Exception as ex:
			print(f"Failed to write to term acceptance file. {ex}")
			exit(1)
	else:
		print("Terms were declined, exiting.")
		exit(0)