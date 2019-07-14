from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class CustomisedWebDriver(webdriver.Chrome):
	def SendKeys(self, inputData):
		self.currentElement.clear()
		self.currentElement.send_keys(inputData)
		self.currentElement.send_keys(Keys.RETURN)

	def Click(self):
		self.currentElement.click()

	def LocateByPath(self, locatorString):
		webWait = WebDriverWait(self, 60)
		element = webWait.until(expected_conditions.element_to_be_clickable((By.XPATH, locatorString)))
		self.currentElement = element

	def LaunchURL(self, urlToLaunch):
		#self.set_window_position(-10000,0)
		self.implicitly_wait(20)
		self.get(urlToLaunch)

	def GetAuthCode(self):
		return self.find_element_by_tag_name("textarea").text