from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Webscraper():
	"""
	Defines functionality for webscraping dictionary definitions
	"""

	def __init__(self, dictionary):
		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.driver = webdriver.Chrome(options=options)
		self.dictionaries = {
			"dwds": ["https://dwds.de/wb/", self.parse_dwds_response]
		}
		self.dictionary = dictionary

	def search_dict_for(self, word):
		self.driver.get(self.dictionaries[self.dictionary][0] + word)
		return self.dictionaries[self.dictionary][1]()

	def parse_dwds_response(self):
		return [x.text for x in self.driver.find_elements(By.CLASS_NAME, "dwdswb-lesart-def")]





if __name__ == "__main__":
	webscraper = Webscraper("dwds")
	print(webscraper.search_dict_for("Gut"))
	print(webscraper.search_dict_for("Prolet"))