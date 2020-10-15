from .emoji import Emoji

class Reaction:

	"""
	Represent a reaction on a message

	count:
		The number of times this emoji was added
	me:
		If the user reacted with this emoji
	emoji: :class:`Emoji`
		The emoji of the reaction
	message:
		The message of the reaction
	"""

	def __init__(self,reaction,message):
		self.count = reaction.get("count")
		self.me = reaction.get("me")
		self.emoji = Emoji(reaction["emoji"])
		self.message = message