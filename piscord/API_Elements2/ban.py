from .channel import User

class Ban:

	"""
	Represent a guild ban

	reason:
		The reason of the ban
	user: :class:`User`
		The banned user
	"""

	def __init__(self,ban,bot):
		self.reason = ban.get("reason")
		self.user = User(ban["user"],bot)
		self.__bot = bot

	def pardon(self, guild_id):

		"""
		Unban the user
		"""

		self.__bot.api(f"/guilds/{guild_id}/bans/{self.user.id}","DELETE")