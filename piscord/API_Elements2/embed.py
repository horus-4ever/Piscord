from .utilities import API_Element

class Embed(API_Element):

	"""
	Represent a message Embed

	Params when you send a Embed:
	https://discord.com/developers/docs/resources/channel#create-message-params

	title:
		The title of the embed

		Max : 256 characters
	type:
		Type of embed

		Embed types should be considered deprecated and might be removed

			- "rich" : Generic Embed
			- "image" : Image Embed
			- "video" : Video Embed
			- "gifv" : Animated gif image Embed rendered as a video Embed 
			- "article" : Article Embed
			- "link" : Link Embed
	description:
		The description of the embed

		Max : 2048 characters
	url:
		Url of the Embed
	timestamp:
		Timestamp of Embed content
	color:
		Decimal value of the Embed color
	footer: :class:`Embed_Footer`
		The footer of the Embed
	image: :class:`Embed_Image`
		The image of the Embed
	thumbnail: :class:`Embed_Image`
		The thumbnail of the Embed
	video: :class:`Embed_Image`
		The video of the Embed
	provider: :class:`Embed_Provider`
		The provider of the Embed
	author: :class:`Embed_Author`
		The author informations of the Embed
	fields: :class:`Embed_Field`
		List of Embed fields

		Max : 25
	"""

	def __init__(self,embed={}):
		self.title = embed.get("title")
		self.type = embed.get("type")
		self.description = embed.get("description")
		self.url = embed.get("url")
		self.timestamp = embed.get("timestamp")
		self.color = embed.get("color")
		self.footer = Embed_Footer(embed.get("footer",{}))
		self.image = Embed_Image(embed.get("image",{}))
		self.thumbnail = Embed_Image(embed.get("thumbnail",{}))
		self.video = Embed_Image(embed.get("video",{}))
		self.provider = Embed_Provider(embed.get("provider",{}))
		self.author = Embed_Author(embed.get("author",{}))
		self.fields = [Embed_Field(field) for field in embed.get("fields",[])]

	def add_field(self,**kwargs):

		"""
		Used to add a field on the Embed

		Return the field
		"""

		self.fields.append(Embed_Field(kwargs))
		return self.fields[-1]


class Embed_Footer(API_Element):

	"""
	Represent the footer of an Embed

	text:
		The text of the footer
	icon_url:
		The url of the footer icon
	proxy_icon_url:
		Same than icon_url, but proxied
	"""

	def __init__(self,footer):
		self.text = footer.get("text")
		self.icon_url = footer.get("icon_url")
		self.proxy_icon_url = footer.get("proxy_icon_url")


class Embed_Image(API_Element):

	"""
	Represent a Embed Image, Embed Thumbnail and Embed Video

	url:
		The url of the image/video
	proxy_url:
		Same than url, but proxied. Video Dmbed does not have this attribute
	height:
		The height of the image
	width:
		The width of the image
	"""

	def __init__(self,image):
		self.url = image.get("url")
		self.proxy_url = image.get("proxy_url")
		self.height = image.get("height")
		self.width = image.get("width")


class Embed_Provider(API_Element):

	"""
	Represent a Embed Provider

	name:
		The provider name
	url:
		The provider url
	"""

	def __init__(self,provider):
		self.name = provider.get("name")
		self.url = provider.get("url")


class Embed_Author(API_Element):

	"""
	Represent a Embed Author

	name:
		Name of the author field

		Max : 256 characters
	url:
		Url of the author field
	icon_url:
		Url of the icon of the author field
	proxy_icon_url:
		same than icon_url, but proxied
	"""

	def __init__(self,author):
		self.name = author.get("name")
		self.url = author.get("url")
		self.icon_url = author.get("icon_url")
		self.proxy_icon_url = author.get("proxy_icon_url")


class Embed_Field(API_Element):

	"""
	Represent a Embed Field

	name:
		The title of the field

		Max : 256 characters
	value:
		The description of the field

		Max : 1024 characters
	inline:
		If the Embed is inline
	"""

	def __init__(self,field):
		self.name = field.get("name")
		self.value = field.get("value")
		self.inline = field.get("inline")