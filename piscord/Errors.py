class Error(Exception):

	def __init__(self):
		self.error = "Unknown Error"

	def __str__(self):
		return self.error

class PermissionsError(Error):

	def __init__(self):
		self.error = "You do not have permission to do this action"

class BadRequestError(Error):

	def __init__(self):
		self.error = "Your query was incomplete or bad"

class RateLimitedError(Error):

	def __init__(self, retry_after):
		self.error = "You have been rate-limited"
		self.retry_after = retry_after

class TokenError(Error):

	def __init__(self):
		self.error = "The token is not valid"

class ConnexionError(Error):

	def __init__(self, error):
		self.error = f"Connexion Error : {error}"