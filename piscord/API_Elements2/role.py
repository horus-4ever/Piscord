from ..Permission import *

class Role:

	"""
	Represent a Emoji

	id:
		ID of the Emoji
	name:
		The name of the emoji
	color:
		Decimal value of the color
	hoist:
		If the role is pinned in the user listing
	position:
		Position of role in roles list
	permissions:
		Value of role permissions
	managed:
		If role is managed
	mentionable:
		If the role can be mentionned
	guild_id:
		The id of the role guild
	mention:
		The mention of the role
	guild:
		The role guild
	"""

	def __init__(self, role, bot):
		self.id = role.get("id")
		self.name = role.get("name")
		self.color = role.get("color")
		self.hoist = role.get("hoist")
		self.position = role.get("position")
		self.permissions = Perm(role.get("permissions",0))
		self.managed = role.get("managed")
		self.mentionable = role.get("mentionable")
		self.guild_id = role.get("guild_id")
		self.__bot = bot

		self.mention = f"<@&{self.id}>"

		self.guild = bot.get_element(bot.guilds,id=self.guild_id)

	def __repr__(self):
		return self.name

	def delete(self):

		"""
		Remove the role
		"""

		self.__bot.api(f"/channels/{self.guild_id}/roles/{self.id}","DELETE")

	def edit(self,**modifs):

		"""
		Modify role, with parameters.
		Parameters : https://discord.com/developers/docs/resources/guild#modify-guild-role
		"""

		self.__bot.api(f"/channels/{self.guild_id}/messages/{self.id}","PATCH",json=modifs)