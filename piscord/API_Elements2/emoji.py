from .utilities import API_Element

class Emoji(API_Element):

	"""
	Represent a Emoji

	id:
		ID of the Emoji
	name:
		The name of the emoji
	roles: :class:`Role`
		Roles this emoji is whitelisted to
	user: :class:`User`
		User that created this emoji
	require_colons:
		If the emoji must be wrapped in colons
	managed:
		If emoji is managed
	animated:
		If the emoji is animated
	available:
		If the emoji can be used
	"""

	def __init__(self,emoji):
		self.id = emoji.get("id")
		self.name = emoji.get("name")
		self.roles = emoji.get("roles")
		self.user = emoji.get("user")
		self.require_colons = emoji.get("require_colons")
		self.managed = emoji.get("managed")
		self.animated = emoji.get("animated")
		self.available = emoji.get("available")

		self.react = f"{self.name}:{self.id}" if self.id else self.name

	def __str__(self):
		if self.id:
			return f"<:{self.name}:{self.id}>"
		return self.name