class ConfigErrorException(Exception):
	# Raised when config.json contains an invalid setting
	def __init__(self, error_src="default", adtl_info=""):
		self.error_src = error_src
		self.adtl_info = adtl_info
		error_msg = "Error detected in config.json at: " + self.error_src + "\nAdditional context: " + self.adtl_info
		super().__init__(error_msg)

class InvalidLanguageException(ConfigErrorException):
	# Exception for unsupported language in config.json
	def __init__(self, lang):
		self.lang = lang
		super().__init__("language", "The only currently supported language is english. Please change the 'lang' parameter in config.json to 'en'") 

class InvalidStyleException(ConfigErrorException):
	# Exception for style that currently does not exist
	def __init__(self, style):
		self.style = style
		super().__init__("style", "The only currently supported style is default. Please change the 'style' parameter in config.json to 'default'")