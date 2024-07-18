import re

def extract_user_ids(string:str):
	"""Extracts user IDs from a string containing <@UserId> or <@!UserId> mentions.

	Args:
		prompt: The string to extract user IDs from.

	Returns:
		A list of extracted user IDs.
	"""
	regex = r"<@!?(\d+)>"
	matches = re.findall(regex, string)
	return matches