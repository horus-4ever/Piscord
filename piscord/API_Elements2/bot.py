from .guild import Guild
from .channel import User

class Bot_Element:

	"""
	Represent the Bot

	user: :class:`User`
		The user corresponding to the bot (name, id, avatar)
	guilds: :class:`Guild`
		List of guilds where the bot is
	relationships:
		List of relationships of the bot (useless for real bot)
	private_channels: :class:`Channel`
		List of private channels of the bot
	presences:
		Not implemented : Presences of the users
	voices:
		List of Voice connexion of the bot

	"""

	def __init__(self, bot_element, bot):
		self.user = User(bot_element.get("user",{}), bot)
		self.guilds = [Guild(guild, bot) for guild in bot_element.get("guilds",[])]
		self.relationships = bot_element.get("relationships",[])
		self.private_channels = bot_element.get("private_channels",[])
		self.presences = bot_element.get("presences",[])
		self.voices = {}

	def __str__(self):
		return self.user.name

	def edit(self,**modifs):

		"""
		Modify bot user, with parameters.
		Parameters : https://discord.com/developers/docs/resources/user#modify-current-user
		"""

		self.api(f"/users/@me","PATCH",json=modifs)

	def create_guild(self,**kwargs):

		"""
		Create a guild channel, with parameters.
		Parameters : https://discord.com/developers/docs/resources/guild#create-guild

		Return :class:`Guild`
		"""

		return Guild(self.api(f"/guilds", "POST", json=kwargs),self)