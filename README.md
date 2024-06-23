# Skidisher Skidtru

Discord user app, written by OCbwoy3!

This is Open Source, so you can make your own version of it, but please give credit.

If you're not planning to run your own PrikolsHub (or a remake/clone of it), feel free to delete `SecLoad.py`, the PrikolsHub `CommandGroup` and `SECLOAD_API_KEY`. Also make sure to update `main.py`.

Also, there is a music sharing command. Self explanatory, shows you a embed of what you're listening to. Please rename `ocbwoy3` in `registrate.py` to something else to not do confusion.

> [!WARNING]
> Abusing PrikolsHub's, SecLoad's and Karma's API will in most cases result a blacklist.

## Enviorment files

`config.py`
```py
WHITELIST = [
	# Put in Discord User IDs of the people who should get whitelist.
]
AI_ACCESS = [
	# UserIDs who should access AI features
]

SECLOAD_API_KEY = "" # https://secload.scriptlang.com/docs leave this blank to disable
GROQ_API_KEY = "" # https://console.groq.com/keys leave this blank to disable
```

`.env`
```
LASTFM_API_KEY=
LASTFM_SHARED_SECRET=
LASTFM_USERNAME=
LASTFM_PASSWORD=
DISCORD_TOKEN=
```
