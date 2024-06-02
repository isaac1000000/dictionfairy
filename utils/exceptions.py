class ConfigErrorException(Exception):
	def __init__(self, error_src="default"):
		self.error_src = error_src
		error_msg = "Error detected in config.json at: " + self.error_src
		super().__init__(error_msg)
