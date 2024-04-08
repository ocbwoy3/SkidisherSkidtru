# Skidisher Skidtru

Discord user app, written by OCbwoy3!

Requires the `feature/user_apps` branch of [`discord.py`](https://github.com/Rapptz/discord.py/tree/feature/user_apps "feature/user_apps"), `uwuipy`, `cfscrape`, `requests`, and idk what more.

If you're not planning to run your own PrikolsHub (or a remake of it), feel free to delete `SecLoad.py`, the PrikolsHub `CommandGroup` and `SECLOAD_API_KEY`. Also make sure to update `main.py`.

Also, there is a music sharing command. Self explanatory, shows you a embed of what you're listening to. Please rename `ocbwoy3` in `registrate.py` to something else to not do confusion!!!

## Enviorment files

`config.py`
```py
WHITELIST = [
	# Put in Discord User IDs of the people who should get whitelist.
]

SECLOAD_API_KEY = "" # unused rn idk
# Get your key here: https://secload.scriptlang.com/docs
```

`.env`
```
LASTFM_API_KEY=
LASTFM_SHARED_SECRET=
LASTFM_USERNAME=
LASTFM_PASSWORD=
DISCORD_TOKEN=
```
