from .role import Role
from .emoji import Emoji
from .channel import Channel, Member, User, Webhook
from .ban import Ban
from ..Permission import *

class Guild:

	"""
	Represent a discord server
	
	id:
		ID of the Guild
	name:
		Name of the Guild
	icon:
		The icon (image show on the guilds menu) of the Guild
	splash:
		The background invite image of the Guild
	discovery_splash:
		The background invite image of the Guild in discovery tab
	owner:
		If the user is the owner of the guild (see : https://discord.com/developers/docs/resources/user#get-current-user-guilds)
	owner_id:
		If owner is not specified, the owner id of the Guild
	permissions:
		The permissions in Guild for the user (see : https://discord.com/developers/docs/resources/user#get-current-user-guilds)
	region:
		Not implemented : Voice region of the guild
	afk_channel_id:
		The id of the afk voice channel
	afk_timeout:
		The time before an inactive user is sent to the afk voice channel
	embed_enabled:
		If the server widget is enabled (deprecated, replaced with widget_enabled)
	embed_channel_id:
		The channel id where the widget generate an invite (deprecated, replaced with widget_channel_id)
	verification_level:
		The level of verification of the server
			- 0 : Unrestricted
			- 1 : Need email verified
			- 2 : Register longer than 5 minutes
			- 3 : In the guild longer than 10 minutes
			- 4 : Require verified phone number
	default_message_notifications:
		The level of messages notification by default
			- 0 : All messages
			- 1 : Mentions Only
	explicit_content_filter:
		Filter for nsfw content (image)
			- 0 : No filter
			- 1 : Filter just for roleless members
			- 2 : All members
	roles: :class:`Role`
		List of Guild roles
	emojis: :class:`Emoji`
		List of Guild emojis
	features:
		Not implemented
	mfa_level:
		If the guild requiere MFA
			- 0 : No
			- 1 : Yes
	application_id:
		If a bot created the server, the id of its application
	widget_enabled:
		If the server widget is enabled
	widget_channel_id:
		The channel id where the widget generate an invite
	system_channel_id:
		The id of channel system messages (boost, welcome)
	system_channel_flags:
		A integer representing the system messages enable
			0 : All system messages
			1 : Boost notification messages
			2 : Welcome messages
			3 : No system messages
	rules_channel_id:
		The id of rules channel for public guilds
	joined_at:
		The timestamp of guild creation
	large:
		If the guild  is considered a large guild
	unavailable:
		If the guild is unavaible
	member_count:
		The number of guild members
	voice_states:
		Not implemented
	members: :class:`Member`
		List of guild members
	channels: :class:`Channel`
		List of guild channels
	presences:
		Not implemented
	max_presences:
		Max number of presence for the guild, 25000 by default
	max_members:
		Max number of members for the guild
	max_video_channel_users:
		Max number of users in a video channel
	vanity_url_code:
		Custom url for discord parteners and guild level 3
	description:
		Guild description in discover tab
	banner:
		Banner of the guild
	premium_tier:
		The level of server boosting:
			- 0 : Level 0
			- 1 : Level 1
			- 2 : Level 2
			- 3 : Level 3
	premium_subscription_count:
		The number of guild nitro boosts
	preferred_locale:
		The preferred locale of a public guild (for discovery tab)
	public_updates_channel_id:
		The staff channel for Discord notices of a public guild
	approximate_member_count:
		The approximate number of guild members
	approximate_presence_count:
		The approximate number of connected guild members
	"""

	def __init__(self, guild, bot):
		self.id = guild.get("id")
		self.name = guild.get("name")
		self.icon = guild.get("icon")
		self.splash = guild.get("splash")
		self.discovery_splash = guild.get("discovery_splash")
		self.owner = guild.get("owner")
		self.owner_id = guild.get("owner_id")
		self.permissions = Perm(guild.get("permissions",0))
		self.region = guild.get("region")
		self.afk_channel_id = guild.get("afk_channel_id")
		self.afk_timeout = guild.get("afk_timeout")
		self.embed_enabled = guild.get("embed_enabled")
		self.embed_channel_id = guild.get("embed_channel_id")
		self.verification_level = guild.get("verification_level")
		self.default_message_notifications = guild.get("default_message_notifications")
		self.explicit_content_filter = guild.get("explicit_content_filter")
		self.roles = [Role(role,bot) for role in guild.get("roles",[])]
		self.emojis = [Emoji(emoji) for emoji in guild.get("emojis",[])]
		self.features = guild.get("features",[]) #To Do
		self.mfa_level = guild.get("mfa_level")
		self.application_id = guild.get("application_id")
		self.widget_enabled = guild.get("widget_enabled")
		self.widget_channel_id = guild.get("widget_channel_id")
		self.system_channel_id = guild.get("system_channel_id")
		self.system_channel_flags = guild.get("system_channel_flags")
		self.rules_channel_id = guild.get("rules_channel_id")
		self.joined_at = guild.get("joined_at")
		self.large = guild.get("large")
		self.unavailable = guild.get("unavailable")
		self.member_count = guild.get("member_count")
		self.voice_states = guild.get("voice_states")
		self.members = [Member({**member,"guild_id":self.id},bot) for member in guild.get("members",[])]
		self.channels = [Channel(channel, bot, guild=self) for channel in guild.get("channels",[])]
		self.presences = guild.get("presences",[]) # To Do
		self.max_presences = guild.get("max_presences",25000)
		self.max_members = guild.get("max_members")
		self.max_video_channel_users = guild.get("max_video_channel_users")
		self.vanity_url_code = guild.get("vanity_url_code")
		self.description = guild.get("description")
		self.banner = guild.get("banner")
		self.premium_tier = guild.get("premium_tier")
		self.premium_subscription_count = guild.get("premium_subscription_count")
		self.preferred_locale = guild.get("preferred_locale")
		self.public_updates_channel_id = guild.get("public_updates_channel_id")
		self.approximate_member_count = guild.get("approximate_member_count")
		self.approximate_presence_count = guild.get("approximate_presence_count")
		self.__bot = bot

	def __repr__(self):
		if self.name:
			return self.name
		elif self.id:
			return self.id
		else:
			return "Guild"

	def edit(self,**modifs):

		"""
		Modify guild, with parameters.
		Parameters : https://discord.com/developers/docs/resources/guild#modify-guild
		"""

		self.__bot.api(f"/guilds/{self.id}","PATCH",json=modifs)

	def delete(self):

		"""
		Delete permanently the guild. The bot must be the owner
		"""

		self.__bot.api(f"/guilds/{self.id}","DELETE")

	def get_channels(self):

		"""
		Return a list of :class:`Channel` of the guild (deprecated, use Guild.channels)
		"""

		channels = self.__bot.api(f"/guilds/{self.id}/channels")
		return [Channel(channel,self.__bot) for channel in channels]

	def get_roles(self):

		"""
		Return a list of :class:`Role` of the guild (deprecated, use Guild.roles)
		"""

		roles = self.__bot.api(f"/guilds/{self.id}/roles")
		return [Role(role,self.__bot) for role in roles]

	def get_invites(self):

		"""
		Return a list of :class:`Invite` of the guild
		"""

		invites = self.__bot.api(f"/guilds/{self.id}/invites")
		return [Invite(invite,self.__bot) for invite in invites]

	def get_members(self, limit=100, after=0):

		"""
		Return a list of :class:`Member` of the guild (deprecated, use Guild.members)
		"""

		members = self.__bot.api(f"/guilds/{self.id}/members","GET",params={"limit":limit,"after":after})
		return [Member({**member,"guild_id":self.id},self.__bot) for member in members]

	def get_member(self,user_id):

		"""
		returns a specific :class:`Member` using their id
		"""

		return Member({**self.__bot.api(f"/guilds/{self.id}/members/{user_id}"),"guild_id":self.id},self.__bot)

	def get_bans(self):

		"""
		Return a list of :class:`Ban` of the guild
		"""

		bans = self.__bot.api(f"/guilds/{self.id}/bans")
		return [Ban(ban,self.__bot) for ban in bans]

	def get_ban(self, user_id):

		"""
		returns a specific :class:`Ban` using the id of the banned user
		"""

		return Ban(self.__bot.api(f"/guilds/{self.id}/bans/{user_id}"),self.__bot)

	def get_webhooks(self):

		"""
		Return a list of :class:`Webhook` of the guild
		"""

		webhooks = self.__bot.api(f"/guilds/{self.id}/webhooks")
		return [Webhook(webhook,self.__bot) for webhook in webhooks]

	def create_channel(self,**kwargs):

		"""
		Create a guild channel, with parameters.
		Parameters : https://discord.com/developers/docs/resources/guild#create-guild-channel

		Return :class:`Channel`
		"""

		return Channel(self.__bot.api(f"/guilds/{self.id}/channels", "POST", json=kwargs),self.__bot)

	def create_role(self,**kwargs):

		"""
		Create a guild role, with parameters.
		Parameters : https://discord.com/developers/docs/resources/guild#create-guild-role

		Return :class:`Role`
		"""

		return Role({**self.__bot.api(f"/guilds/{self.id}/roles", "POST", json=kwargs),"guild_id":self.id},self.__bot)

	def count_prune(self, days=7, include_roles=[]):
		
		"""
		Count the number of users will be pruned if you start a prune

		days:
			The number of days the user need to be inactive to be counted
		include_roles:
			The roles to be considered to prune (by default, a user with a role can't be pruned)
		"""

		self.__bot.api(f"/guilds/{self.id}/prune", "GET", params={"days":days,"include_roles":include_roles})

	def prune(self, days=7, include_roles=[]):

		"""
		Prune inactive members (kick)

		days:
			The number of days the user need to be inactive to be counted
		include_roles:
			The roles to be considered to prune (by default, a user with a role can't be pruned)
		"""

		self.__bot.api(f"/guilds/{self.id}/prune", "POST", params={"days":days,"include_roles":include_roles})


class Invite:

	"""
	Represent a guild invite

	code:
		The code of the invite (For example, code U9X7XzP corresponding to invitation https://discord.gg/U9X7XzP)
	guild: :class:`Guild`
		A partial guild object : The guild of the invite
	channel: :class:`Channel`
		A partial channel object : The channel of the invite
	inviter: :class:`User`
		The user who created the invite
	target_user: :class:`User`
		The target user for the invite
	target_user_type:
		The type of user target for the invite
			1 : Stream
	approximate_presence_count:
		The approximate number of connected users in the guild
	approximate_member_count:
		The approximate number of users in the guild
	url:
		The url of the invite
	uses:
		The number of invite uses
	max_uses:
		The number of max invite uses
	max_age:
		The time before invite is automatically deleted
	temporary:
		If the invite give temporary membership
	created_at:
		Timestamp when the invite was created
	"""

	def __init__(self, invite, bot):
		self.code = invite.get("code")
		self.url = f"https://discord.gg/{self.code}"
		self.guild = None
		if "guild" in invite:
			self.guild = Guild(invite["guild"], bot)
		self.channel = None
		if "channel" in invite:
			self.channel = Channel(invite["channel"], bot)
		self.inviter = None
		if "inviter" in invite:
			self.inviter = User(invite["inviter"], bot)
		self.target_user = None
		if "target_user" in invite:
			self.channel = User(invite["target_user"], bot)
		self.target_user_type = invite.get("target_user_type")
		self.approximate_presence_count = invite.get("approximate_presence_count")
		self.approximate_member_count = invite.get("approximate_member_count")
		self.uses = invite.get("uses")
		self.max_uses = invite.get("max_uses")
		self.max_age = invite.get("max_age")
		self.temporary = invite.get("temporary")
		self.created_at = invite.get("created_at")
		self.__bot = bot

	def __repr__(self):
		return self.url

	def delete(self):

		"""
		Delete the invite
		"""

		self.__bot.api(f"/invites/{self.code}","DELETE")