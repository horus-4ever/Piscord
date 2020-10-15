from .overwrite import Overwrite
from .attachement import Attachment
from .reaction import Reaction
from .embed import Embed
from .utilities import Cache

from enum import IntEnum


class CHANNEL_TYPE(IntEnum):
    TEXT_CHANNEL = 0
    DM_CHANNEL = 1
    VOICE_CHANNEL = 2
    DM_GROUP_CHANNEL = 3
    CATEGORY_CHANNEL = 4
    NEWS_CHANNEL = 5
    STORE_CHANNEL = 6
    DEFAULT = 7


class Channel:

    """
    Represent a discord channel

    id:
        ID of the Channel
    type:
        The type of the channel
            0 : Text channel of a Guild
            1 : DM channel
            2 : Voice channel of a Guild
            3 : DM group channel
            4 : Category
            5 : News channel
            6 : Store channel
    guild_id:
        The guild id of the channel (if is not a dm channel)
    position:
        The channel position in the guild channels
    permission_overwrites:
        The permissions for members and roles in the channel
    name:
        Name of the channel
    topic:
        The channel topic
    nsfw:
        If the channel is or not a nsfw channel
    last_message_id:
        The id of the last channel message
    bitrate:
        The bitrate of the channel (if this is a voice channel)
    user_limit:
        The limit of users in the channel (if this is a voice channel)
    rate_limit_per_user:
        The time between two messages, in seconds
    recipients: :class:`User`
        The DM group users
    icon:
        The icon of the DM group
    owner_id:
        The id of the DM group owner
    application_id:
        If a bot created the DM group, the id of its application
    parent_id:
        If the channel is in a category, the category id
    last_pin_timestamp:
        timestamp when the last pinned message was pinned
    invites: :class:`Invite`
        List of channel invites
    mention:
        The mention of the channel
    guild: :class:`Guild`
        The guild of the channel
    """

    def __new__(cls, channel, bot, guild=None):
        type_ = channel["type"]
        if type_ == CHANNEL_TYPE.TEXT_CHANNEL:
            channel_type = TextChannel
        elif type_ == CHANNEL_TYPE.VOICE_CHANNEL:
            channel_type = VoiceChannel
        elif type_ == CHANNEL_TYPE.CATEGORY_CHANNEL:
            channel_type = CategoryChannel
        else:
            channel_type = DefaultChannel
        return object.__new__(channel_type)

    def __init__(self, channel, bot, guild=None):
        self.id = channel.get("id")
        self.type = channel.get("type")

        self.__bot = bot
        self.mention = f"<#{self.id}>"

        if guild is not None:
            self.guild = guild
        else:
            self.guild = bot.get_element(bot.guilds, id=self.guild_id)

    def __repr__(self):
        return f"{self.__class__.__name__}(\"{self.name or self.id}\")"

    def __init_subclass__(cls):
        if not hasattr(cls, "__channel_type__"):
            cls.__channel_type__ = CHANNEL_TYPE.DEFAULT


class TextChannel(Channel):

    __channel_type__ = CHANNEL_TYPE.TEXT_CHANNEL

    def __init__(self, channel, bot, guild=None):
        super().__init__(channel, bot, guild)
        self.guild_id = channel.get("guild_id")
        self.position = channel.get("position")
        self.permission_overwrites = [Overwrite(
            overwrite, bot, self.id) for overwrite in channel.get("permission_overwrites", [])]
        self.name = channel.get("name")
        self.topic = channel.get("topic")
        self.nsfw = channel.get("nsfw")
        self.last_message_id = channel.get("last_message_id")
        self.rate_limit_per_user = channel.get("rate_limit_per_user")
        self.parent_id = channel.get("parent_id")
        self.last_pin_timestamp = channel.get("last_pin_timestamp")

    def edit(self,**modifs):

        """
        Modify channels, with parameters.
        Parameters : https://discord.com/developers/docs/resources/channel#modify-channel
        """

        self.__bot.api(f"/channels/{self.id}","PATCH",json=modifs)

    def send(self,content=None,files=None,**kwargs):

        """
        Send a message in the channels, with parameters.
        Parameters : https://discord.com/developers/docs/resources/channel#create-message

        By default, when not kwarg specified, arg is the content.

        Use send(files=["name_1","name_2"]) to send files by their names
        
        Use send(files=[[b"data_2","title_1"],[b"data_2","title_2"]]) to send files by their data

        Return :class:`Message`
        """

        if files is not None:
            form = aiohttp.FormData()
            form.add_field('payload_json', json.dumps({"content":content,**kwargs}))
            for i, file in enumerate(files):
                if type(file) == str:
                    filename = file
                    with open(filename,"rb") as f:
                        file_content = f.read()
                elif type(file) == list:
                    file_content, filename = file
                else:
                    raise TypeError("Files should be a list or a string")
                form.add_field(f"file {i}", file_content, filename=filename)
            return Message(self.__bot.api(f"/channels/{self.id}/messages", "POST", data=form),self.__bot)
        else:
            return Message(self.__bot.api(f"/channels/{self.id}/messages", "POST", json={"content":content,**kwargs}),self.__bot)

    def get_messages(self,limit=50,before=None,after=None):

        """
        Get list of messages in the channel

        limit:
            The max number of messages return (max : 100)
        before:
            ID of a message : Retrieves messages that are before the message
        after:
            ID of a message : Retrieves messages that are after the message

        Return List of :class:`Message`
        """
        params = {"limit":limit}
        if before:
            params["before"] = before
        if after:
            params["after"] = after

        messages = self.__bot.api(f"/channels/{self.id}/messages","GET",params=params)
        return [Message(message,self.__bot) for message in messages]

    def get_message(self,message_id):

        """
        Get specific message of the channel with it id

        Return :class:`Message`
        """

        return Message(self.__bot.api(f"/channels/{self.id}/messages/{message_id}"),self.__bot)

    def get_invites(self):

        """
        Get list of invites of the channel

        Return List of :class:`Invite`
        """

        invites = self.__bot.api(f"/channels/{self.id}/invites")
        return [Invite(invite,self.__bot) for invite in invites]

    def get_webhooks(self):

        """
        Get list of webhooks of the channel

        Return List of :class:`Webhook`
        """

        webhooks = self.__bot.api(f"/channels/{self.id}/webhooks")
        return [Webhook(webhook,self.__bot) for webhook in webhooks]

    def create_invite(self,**kwargs):

        """
        Create a guild invite for the channel, with parameters
        Parameters : https://discord.com/developers/docs/resources/channel#create-channel-invite

        Return :class:`Invite`
        """

        return Invite(self.__bot.api(f"/channels/{self.id}/invites","POST",json=kwargs),self.__bot)

    def create_webhook(self,name,avatar=None):

        """
        Create a webhook for the channel
        
        name:
            The name of the webhook
        avatar:
            The avatar image data (see : https://discord.com/developers/docs/reference#image-data) of the webhook

        Return :class:`Webhook`
        """

        return Webhook(self.__bot.api(f"/channels/{self.id}/webhooks","POST",json={"name":name,"avatar":avatar}),self.__bot,channel=self)

    def bulk_delete(self,messages_ids):

        """
        Delete multiple messages

        messages_ids:
            The ids of the message to delete

            Max : 100
        """

        if len(messages_ids) > 100:
            raise ValueError("Max number exceeded")

        self.__bot.api(f"/channels/{self.id}/messages/bulk-delete","POST",json={"messages":messages_ids})

    def purge(self, max, before = None, after = None):

        """
        Delete messages from a channels

        max:
            The number of messages to delete

            Max : 100
        before:
            The messages before a message id
        after:
            The messages after a message id
        """

        if max > 100:
            raise ValueError("Max number exceeded")

        messages = [message.id for message in self.get_messages(limit=max,before=before,after=after)]
        self.bulk_delete(messages)

    def typing(self):

        """
        Send a "typing" event in the channel ('bot typing...') until the bot sends a message
        """

        self.__bot.api(f"/channels/{self.id}/typing","POST")
        

class VoiceChannel(Channel):

    __channel_type__ = CHANNEL_TYPE.VOICE_CHANNEL

    def __init__(self, channel, bot, guild=None):
        super().__init__(channel, bot, guild)
        self.guild_id = channel.get("guild_id")
        self.position = channel.get("position")
        self.permission_overwrites = [Overwrite(overwrite,bot,self.id) for overwrite in channel.get("permission_overwrites",[])]
        self.name = channel.get("name")
        self.nsfw = channel.get("nsfw")
        self.parent_id = channel.get("parent_id")
        self.bitrate = channel.get("bitrate")
        self.user_limit = channel.get("user_limit")

    def join(self):
        """
        Join the voice channel
        """
        raise NotImplementedError()


class CategoryChannel(Channel):

    __channel_type__ = CHANNEL_TYPE.CATEGORY_CHANNEL

    def __init__(self, channel, bot, guild=None):
        super().__init__(channel, bot, guild)
        self.guild_id = channel.get("guild_id")
        self.position = channel.get("position")
        self.permission_overwrites = [Overwrite(overwrite,bot,self.id) for overwrite in channel.get("permission_overwrites",[])]
        self.name = channel.get("name")
        self.nsfw = channel.get("nsfw")
        self.parent_id = channel.get("parent_id")


class DMChannel(TextChannel):

    __channel_type__ = CHANNEL_TYPE.DM_CHANNEL


class DefaultChannel(Channel):

    def __init__(self, channel, bot, guild=None):
        self.id = channel.get("id")
        self.type = channel.get("type")
        self.guild_id = channel.get("guild_id")
        self.position = channel.get("position")
        self.permission_overwrites = [Overwrite(overwrite,bot,self.id) for overwrite in channel.get("permission_overwrites",[])]
        self.name = channel.get("name")
        self.topic = channel.get("topic")
        self.nsfw = channel.get("nsfw")
        self.last_message_id = channel.get("last_message_id")
        self.bitrate = channel.get("bitrate")
        self.user_limit = channel.get("user_limit")
        self.rate_limit_per_user = channel.get("rate_limit_per_user")
        self.recipients = [User(user,bot) for user in channel.get("recipients",[])]
        self.icon = channel.get("icon")
        self.owner_id = channel.get("owner_id")
        self.application_id = channel.get("application_id")
        self.parent_id = channel.get("parent_id")
        self.last_pin_timestamp = channel.get("last_pin_timestamp")
        self.invites = channel.get("invites",[])


class Message:

    """
    Represent a message send in a channel by a user

    id:
        ID of the message
    channel_id:
        ID of the channel where the message is
    guild_id: 
        ID of the guild where the message is (if is not a DM)
    author: :class:`User` or :class:`Member`
        A user object of the author. If the channel is not a DM, this is a member object
    content:
        The content of the message
    timestamp:
        The timestamp when the message was sent
    edited_timestamp:
        The timestamp when the message was edited
    tts:
        If the message was a TTS message
    mention_everyone:
        If the message mention everyone
    mentions: :class:`User`
        List of users mentionned in the message
    mention_roles: :class:`Role`
        List of roles mentionned in the message
    mention_channels: :class:`Channel`
        List of channels mentionned in the message

        (incomplete object, see : https://discord.com/developers/docs/resources/channel#channel-mention-object)
    attachments: :class:`Attachement`
        List of attachments of the message
    embeds: :class:`Embed`
        If the message have embeds, list of embeds in the message
    reactions: :class:`Reaction`
        List of reactions of the message
    nonce:
        Nonce of the message
    pinned:
        If the message is pinned
    webhook_id:
        Webhood id if the message was generated by a webhook
    type:
        The type of message
            - 0 : A normal message
            - 1 : A DM group member add
            - 2 : A DM group member remove
            - 3 : A DM call start
            - 4 : A change of DM group channel name
            - 5 : A change of DM group channel icon
            - 6 : A channel pin
            - 7 : A guild member arrival
            - 8 : A guild boost
            - 9 : A guild boost tier 1
            - 10 : A guild boost tier 2
            - 11 : A guild boost tier 3
            - 12 : A channel follow add
            - 13 : A guild discovery disqualified
            - 14 : A guild discovery requalified
    activity:
        Not implemented
    application:
        Not implemented
    message_reference:
        Not implemented
    flags:
        Message flags (see : https://discord.com/developers/docs/resources/channel#message-object-message-flags)
    guild: :class:`Guild`
        The guild where the message was sent (if is not in DM)
    channel: :class:`Channel`
        The channel where the message was sent
    """

    def __init__(self, message, bot):
        self.id = message.get("id")
        self.channel_id = message.get("channel_id")
        self.guild_id = message.get("guild_id")
        self.author = None
        if "author" in message:
            self.author = User(message["author"],bot)
        if "member" in message:
            self.author = Member({**message["member"],"user":{**message["author"]},"guild_id":self.guild_id}, bot)
        self.content = message.get("content")
        self.timestamp = message.get("timestamp")
        self.edited_timestamp = message.get("edited_timestamp")
        self.tts = message.get("tts")
        self.mention_everyone = message.get("mention_everyone")
        self.mentions = [User(mention,bot) for mention in message.get("mentions",[])]
        self.mentions_roles = message.get("mention_roles")
        self.mention_channels = [Channel(channel,bot) for channel in message.get("mention_channels",[])]
        self.attachments = [Attachment(attachment) for attachment in message.get("attachments",[])]
        self.embeds = [Embed(embed) for embed in message.get("embeds",[])]
        self.reactions = [Reaction(reaction,self) for reaction in message.get("reactions",[])]
        self.nonce = message.get("nonce")
        self.pinned = message.get("pinned")
        self.webhook_id = message.get("webhook_id")
        self.type = message.get("type")
        self.activity = message.get("activity") # Object
        self.application = message.get("application") #Object
        self.message_reference = message.get("message_reference") #Object
        self.flags = message.get("flags")
        self.__bot = bot

        self.guild = bot.get_element(bot.guilds, id=self.guild_id)
        if self.guild:
            self.channel = bot.get_element(self.guild.channels, id=self.channel_id)
        else:
            self.channel = bot.get_element(bot.private_channels, id=self.channel_id)

    def __repr__(self):
        return self.content

    def delete(self):

        """
        Delete the message
        """

        self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}","DELETE")

    def edit(self,**modifs):

        """
        Modify channels, with parameters.
        Parameters : https://discord.com/developers/docs/resources/channel#edit-message
        """

        self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}","PATCH",json=modifs)

    def add_reaction(self, reaction):

        """
        Add the reaction in the message

        reaction:
            A emoji.react string
        """

        self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","PUT")

    def delete_reactions(self):

        """
        Delete all reactions on the message
        """

        self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions","DELETE")

    def delete_self_reaction(self, reaction):

        """
        Delete its own reaction
        """

        self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","DELETE")

    def delete_reaction(self,reaction,user_id=None):

        """
        If user_id is specified, delete the reaction of a specific user,
        else, delete all the reactions corresponding to the reaction in argument
        """

        if isinstance(reaction, Emoji):
            reaction = reaction.react

        if user_id:
            self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/{user_id}","DELETE")
        else:
            self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}","DELETE")



class User:

    """
    Represent a user of discord

    id:
        ID of the user
    name:
        Username of the user
    discriminator:
        Discriminator of the user
    avatar:
        Avatar link of the user (discord cdn)
    bot:
        If the user is a bot
    system:
        If the user is a Official Discord System user
    mfa_enabled:
        If the user has two factor authentification enabled
    locale:
        The discord language of the user
    verified:
        If the user email is verified
    email:
        The email of the user
    flags:
        The user flags (see: https://discord.com/developers/docs/resources/user#user-object-user-flags)
    premium_type:
        The nitro level of the user
            - 0 : No nitro
            - 1 : Basic nitro
            - 2 : Nitro boost
    public_flags:
        The public flags of the user (see : https://discord.com/developers/docs/resources/user#user-object-user-flags)
    mention:
        The mention of the user
    dm: :class:`Channel`
        The DM channel of the user
    """

    def __init__(self, user, bot):
        self.id = user.get("id")
        self.name = user.get("username")
        self.discriminator = user.get("discriminator")
        self.avatar = user.get("avatar")
        if self.avatar:
            if self.avatar.startswith("a_"):
                avatar_type = ".gif"
            else:
                avatar_type = ".png"
            self.avatar = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}{avatar_type}"
        self.bot = user.get("bot")
        self.system = user.get("system")
        self.mfa_enabled = user.get("mfa_enabled")
        self.locale = user.get("locale")
        self.verified = user.get("verified")
        self.email = user.get("email")
        self.flags = user.get("flags")
        self.premium_type = user.get("premium_type")
        self.public_flags = user.get("public_flags")
        self.mention = f"<@{self.id}>"
        self.__bot = bot

    def __repr__(self):
        return self.name

    @property
    @Cache
    def dm(self):
        return Channel(self.__bot.api(f"/users/@me/channels","POST",json={"recipient_id":self.id}),self.__bot)


class Member(User):

    """
    Member object is a supplement of the :class:`User` class for guild members

    A member is associated with a guild

    It have most often the same basic attribute of :class:`User`

    nick:
        The username of member in the guild
    roles: :class:`Role`
        List of member roles in the guild if the user if the guild is in the bot cache
    roles_id:
        List of the roles id
    hoisted_role:
        Not implemented
    joined_at:
        Timestamp when member join the guild
    premium_since:
        Timestamp when member starting boost the server
    deaf:
        If the member is deafened in voice channels
    mute:
        If the member is muted in voice channels
    guild_id:
        ID of the guild of the member
    guild: :class:`Guild`
        The guild where the member is
    """

    def __init__(self, member, bot):
        if "user" in member:
            User.__init__(self,member["user"],bot)
        self.nick = member.get("nick")
        self.roles_id = member.get("roles",[])
        self.roles = None
        self.hoisted_role = member.get("hoisted_role")
        self.joined_at = member.get("joined_at")
        self.premium_since = member.get("premium_since")
        self.deaf = member.get("deaf")
        self.mute = member.get("mute")
        self.guild_id = member.get("guild_id")
        self.__bot = bot

        self.guild = bot.get_element(bot.guilds,id=self.guild_id)

        if self.guild:
            self.roles = []
            for i in range(len(self.roles_id)):
                role = bot.get_element(self.guild.roles,id=self.roles_id[i])
                if role:
                    self.roles.append(role)

    def edit(self, **modifs):

        """
        Modify member, with parameters.
        Parameters : https://discord.com/developers/docs/resources/guild#modify-guild-member
        """

        if hasattr(self,"id"):
            user_id=self.id
            self.__bot.api(f"/channels/{self.guild_id}/messages/{user_id}","PATCH",json=modifs)

    def kick(self):

        """
        Kick the guild member
        """

        if hasattr(self,"id"):
            user_id=self.id
            delete_member = self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}","DELETE")

    def ban(self, reason=None):

        """
        Ban the guild member
        """

        if hasattr(self,"id"):
            user_id=self.id
            self.__bot.api(f"/guilds/{self.guild_id}/bans/{user_id}","PUT", json={"reason":reason})

    def add_role(self, role):

        """
        Add a role to the guild member

        role: :class:`Role`
            A guild role object
        """

        if hasattr(self,"id"):
            user_id=self.id
            self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}/roles/{role.id}","PUT")

    def remove_role(self, role):

        """
        Remove a role to the guild member

        role: :class:`Role`
            A guild role object
        """

        if hasattr(self,"id"):
            user_id=self.id
            self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}/roles/{role.id}","DELETE")


class Webhook:

    """
    Represent a channel Webhook

    id:
        ID of the webhook
    type:
        The type of the webhook
            - 0 : Incoming webhook
            - 1 : Channel following webhook
    guild_id:
        The id of the webhook guild
    channel_id:
        The id of the webhook channel
    user: :class:`User`
        The user who created the webhook
    name:
        The name of the webhook
    avatar:
        The avatar link of the webhook
    token:
        The webhook secure token (For Incoming Webhooks)
    channel: :class:`Channel`
        The channel of the webhook
    guild:
        The guild of the webhook
    """

    def __init__(self, webhook, bot, channel=None):
        self.id = webhook.get("id")
        self.type = webhook.get("type")
        self.guild_id = webhook.get("guild_id")
        self.channel_id = webhook.get("channel_id")
        self.user = User(webhook.get("user"),{})
        self.name = webhook.get("name")
        self.avatar = webhook.get("avatar")
        self.token = webhook.get("token")
        self.__bot = bot

        if channel:
            self.channel = channel
            self.guild = channel.guild
        else:
            if self.guild_id:
                self.guild = bot.get_element(bot.guilds,id=self.guild_id)
                if self.channel_id:
                    self.channel = bot.get_element(self.guild.channels,id=self.channel_id)

    def send(self,content=None,files=None,**kwargs):

        """
        Send a message with webhook :

        This is like message sending in channel
        """

        if files:
            form = aiohttp.FormData()
            form.add_field('payload_json', json.dumps({"content":content,**kwargs}))
            for i in range(len(files)):
                file = files[i]
                if type(file) == str:
                    with open(file,"rb") as f:
                        c = f.read()
                elif type(file) == list:
                    c = file[0]
                    file = file[1]
                else:
                    raise TypeError("File should be a list or a string")
                form.add_field(f"file {i}", c, filename=file)
            return self.__bot.api(f"/webhooks/{self.id}/{self.token}", "POST", data=form)
        return self.__bot.api(f"/webhooks/{self.id}/{self.token}", "POST", json={"content":content,**kwargs})

    def edit(self,**modifs):

        """
        Modify webhook, with parameters.
        Parameters : https://discord.com/developers/docs/resources/webhook#modify-webhook
        """

        self.__bot.api(f"/webhooks/{self.id}","PATCH",json=modifs)

    def delete(self):

        """
        Delete the webhook
        """

        self.__bot.api(f"/webhooks/{self.id}","DELETE")