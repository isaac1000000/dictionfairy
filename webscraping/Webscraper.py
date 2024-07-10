from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.exceptions import ConfigErrorException

class Webscraper():
	"""
	Defines functionality for webscraping dictionary definitions
	"""
	def __init__(self, dictionary):
		options = webdriver.ChromeOptions()
		options.add_argument("--headless=new")
		options.add_argument("--log-level=1")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = webdriver.Chrome(options=options)
		self.dictionaries = {
			"dwds.de: de-de": ["https://dwds.de/wb/", self.parse_dwds_response],
			"leo: de-en": ["https://dict.leo.org/german-english/", self.parse_leo_response],
			"WordReference: fr-en": ["https://wordreference.com/fren/", self.parse_wr_response]
		}
		if dictionary not in self.dictionaries.keys():
			raise ConfigErrorException("preferred-dictionary")
		self.dictionary = dictionary

	def search_dict_for(self, word):
		self.driver.get(self.dictionaries[self.dictionary][0] + word)
		return self.dictionaries[self.dictionary][1]()

	def parse_dwds_response(self):
		# Parses a response from dwds.de german to german dictionary
		responses = self.driver.find_elements(By.CSS_SELECTOR, ".dwdswb-lesart-def")
		for index, response in enumerate(responses):
			# Retrieve text from elements hidden in case page is multi-tabbed
			if not response.is_displayed():
				responses[index] = str(response.get_attribute("innerText"))
			else:
				responses[index] = response.text
		responses = [response.replace("⟩", ") ").replace("⟨", "(").strip() for response in responses][:15]
		if not responses:
			responses = ["No results"]
		return responses

	def parse_leo_response(self):
		# Parses a response from leo german to english dictionary
		result = []
		# Nouns
		result += [x.text for x in self.driver.find_elements(By.XPATH, """
			//div[@aria-label='Suchergebnisse in der Kategorie Nouns']
			/descendant::td[@lang='en'][not(samp/mark or samp/a/mark)]""")][:5]
		# Adjectives / adverbs
		result += [x.text for x in self.driver.find_elements(By.XPATH, """
			//div[@aria-label='Suchergebnisse in der Kategorie Adjectives / Adverbs']
			/descendant::td[@lang='en'][not(samp/mark or samp/a/mark)]""")][:5]
		# Verbs
		result += [x.text for x in self.driver.find_elements(By.XPATH, """
			//div[@aria-label='Suchergebnisse in der Kategorie Verbs']
			/descendant::td[@lang='en'][not(samp/mark or samp/a/mark)]""")][:5]
		if not result:
			result = ["No results"]
		return result

	def parse_wr_response(self):
		# Parses a response from WordReference french to english dictionary
		result = [x.text for x in self.driver.find_elements(By.XPATH, """
			//tr[not(contains(@class, 'langHeader'))]
			/td[@class='ToWrd']""")][:15]
		if not result:
			result = ["No results"]
		return result

	def set_dictionary(self, dictionary):
		self.dictionary = dictionary

if __name__ == "__main__":
	webscraper = Webscraper("dwds")
	print(webscraper.search_dict_for("gut"))
	print(webscraper.search_dict_for("Prolet"))