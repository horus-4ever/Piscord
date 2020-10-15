from .utilities import API_Element
from ..Permission import Perm

class Overwrite(API_Element):

	"""
	Represent a Overwrite

	id:
		ID of the Overwrite
	type:
		The type of the Overwite
			- "role" : A role Overwrite
			- "member" : A member Overwrite
	allow:
		Permissions allow by Overwrite
	deny:
		Permissions deny by Overwrite
	"""

	def __init__(self,overwrite,bot,channel_id):
		self.id = overwrite.get("id")
		self.type = overwrite.get("type")
		self.allow = Perm(overwrite.get("allow",0))
		self.deny = Perm(overwrite.get("deny",0))
		self.channel_id = channel_id
		self.__bot = bot

	def edit(self,**modifs):

		"""
		Modify overwrite, with parameters.
		Parameters : https://discord.com/developers/docs/resources/channel#edit-channel-permissions
		"""

		self.__bot.api(f"/channels/{self.channel_id}/permissions/{self.id}","PUT",json=modifs)

	def delete(self):

		"""
		Delete overwrite
		"""

		self.__bot.api(f"/channels/{self.channel_id}/permissions/{self.id}","DELETE")