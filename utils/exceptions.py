class ConfigErrorException(Exception):
	def __init__(self, error_src="default", adtl_info=""):
		self.error_src = error_src
		self.adtl_info = adtl_info
		error_msg = "Error detected in config.json at: " + self.error_src + "\nAdditional context: " + self.adtl_info
		super().__init__(error_msg)
