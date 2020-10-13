class Error(Exception):
	error = "Unknown Error"
	def __str__(self):
		return self.error

class PermissionsError(Error):
	error = "You do not have permission to do this action"

class BadRequestError(Error):
	error = "Your query was incomplete or bad"

class TokenError(Error):
	error = "The token is not valid"

class ConnexionError(Error):
	error = "Connexion Error : {}"
	def __init__(self, error):
		self.error = self.error.format(error)