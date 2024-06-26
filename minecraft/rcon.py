from dotenv import load_dotenv
from mcrcon import MCRcon
from os import getenv
from typing import List, Union

load_dotenv()

def replace_color_tag(text: str) -> str:
	color_tags = [
		"§1",
		"§2",
		"§3",
		"§4",
		"§5",
		"§6",
		"§7",
		"§8",
		"§9",
		"§0",
		"§c",
		"§e",
		"§a",
		"§b",
		"§d",
		"§f",
		"§l",
		"§m",
		"§n",
		"§o",
		"§r",
	]
	for char in color_tags:
		text = text.replace(char, "")
	return text

def command_execute(command: str) -> Union[str, List[str]]:
	try:
		with MCRcon(
			getenv("rcon_host"), getenv("rcon_password"), int(getenv("rcon_port"))
		) as mcr:
			mcr.connect()
			response = mcr.command(command)
			return replace_color_tag(response)
	except Exception as e:
		return "Произошла ошибка RCON. Повторите попытку: " + str(e)