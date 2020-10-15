from .utilities import API_Element

class Attachment(API_Element):

	"""
	Represent a message attachment, contain file

	id:
		ID of the attachment
	filename:
		The name of the attachment file
	size:
		The size of the attachment, in bytes
	url:
		Url for get the file
	proxy_url:
		Same than url, but proxied
	height:
		Height of the image attachment (if this is an image)
	width:
		Width of the image attachment (if this is an image)
	"""

	def __init__(self,attachment={}):
		self.id = attachment.get("id")
		self.filename = attachment.get("filename")
		self.size = attachment.get("size")
		self.url = attachment.get("url")
		self.proxy_url = attachment.get("proxy_url")
		self.height = attachment.get("height")
		self.width = attachment.get("width")