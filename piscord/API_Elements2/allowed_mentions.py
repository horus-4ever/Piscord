from .utilities import API_Element

class Allowed_Mentions(API_Element):

	"""
	Represent the mentions allowed for message sending

	parse:
		List of the mentions types allowed
			- "roles" : mentions of roles
			- "users" : mentions of users
			- "everyone" : mentions @everyone and @here
	roles:
		List of id of whitelist roles mentions
	users:
		List of id of whitelist users mentions
	"""

	def __init__(self,mentions={}):
		self.parse = mentions.get("parse")
		self.roles = mentions.get("roles")
		self.users = mentions.get("users")