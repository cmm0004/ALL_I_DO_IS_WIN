import tweepy, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumIntructions(object):
	
	def __init__(self, author, people_to_follow, contest_tweet):
		#[]screen_name, including the author
		self.people_to_follow = people_to_follow
		#id
		self.contest_tweet = contest_tweet
		#screen_name
		self.author = author

class APIKeys(object):
 
	def __init__(self):
		self.consumer_key = os.getenv('CONSUMER_KEY')
		self.consumer_secret = os.getenv('CONSUMER_SECRET')
		self.access_token = os.getenv('ACCESS_TOKEN')
		self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

	def connect(self):
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.secure = True
		self.auth.set_access_token(self.access_token, self.access_token_secret)

		api_connection = tweepy.API(self.auth)

		return api_connection


class Bot(object):

	def __init__(self, APIConnection):
		self.bot = APIConnection


	def search(self, query, lang, count):
		return self._get_statuses(query, lang, count)

		##location = "42.879094,-97.381205,1000mi"
	def _get_statuses(self, query, lang="en", count=5):
		return [status for status in tweepy.Cursor(self.bot.search, q=query, lang=lang).items(count)]

	def filter_already_following(self, people_to_follow):
		relationships = self.bot.lookup_friendships(screen_names=people_to_follow)
		#for each relationship, is we are already following, remove from to_follow list where the screen_name is the same.
		for relationship in relationships:
			if relationship.is_following:
				people_to_follow.remove(relationship.screen_name)
		return people_to_follow




class Selenium(object):

	def __init__(self):
		self.driver = None
	def login(self):
		self.driver = webdriver.Firefox()
		self.driver.get("http://www.twitter.com")
		
		try:
			loginbutton = self.driver.find_element(By.CSS_SELECTOR, "button.js-login")
			loginbutton.click()

			usernameInput = self.driver.find_element(By.CSS_SELECTOR, "input#signin-email")
			passwordInput = self.driver.find_element(By.CSS_SELECTOR, "input#signin-password")
			usernameInput.send_keys("funcmasterc")
			passwordInput.send_keys("Emokid11!")
			passwordInput.submit()
			print('logging in js button')
		except NoSuchElementException as e:
			usernameInput = self.driver.find_element(By.CSS_SELECTOR, "input#signin-email")
			passwordInput = self.driver.find_element(By.CSS_SELECTOR, "input#signin-password")
			usernameInput.send_keys("funcmasterc")
			passwordInput.send_keys("Emokid11!")
			passwordInput.submit()
		except ElementNotVisibleException:
			usernameInput = self.driver.find_element(By.CSS_SELECTOR, "input#signin-email")
			passwordInput = self.driver.find_element(By.CSS_SELECTOR, "input#signin-password")
			usernameInput.send_keys("funcmasterc")
			passwordInput.send_keys("Emokid11!")
			passwordInput.submit()	

		try:
			WebDriverWait(self.driver, 10).until(EC.title_contains("Twitter"))
			
		except TimeoutException:
			raise
			

	def follow_and_retweet(self, selenium_instructions):
		people_to_follow = selenium_instructions.people_to_follow
		contest_tweet = selenium_instructions.contest_tweet
		try:
			self.follow(people_to_follow)
			self.retweet(selenium_instructions)
		except TimeoutException:
			raise
		except ElementNotVisibleException:
			raise
	def follow(self, people_to_follow):
		for screen_name in people_to_follow:

			self.driver.get("http://www.twitter.com/{0}".format(screen_name))
			#if on user page
			try:
				WebDriverWait(self.driver, 10).until(EC.title_contains("@{0}".format(screen_name)))
			except TimeoutException:
				raise
			followbtn = self.driver.find_element(By.CSS_SELECTOR, "button.user-actions-follow-button")
			followbtn.click()

		pass
	def retweet(self, selenium_instructions):
		#on tweet details page
		self.driver.get("http://www.twitter.com/{0}/status/{1}".format(selenium_instructions.author, selenium_instructions.contest_tweet))
		try:
			WebDriverWait(self.driver, 10).until(EC.title_contains("Twitter"))
		except TimeoutException:
			raise
		try:
			retweetIcon = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.Icon.Icon--retweet")))
			retweetIcon.click()
		except TimeoutException:
			raise
		try: 
			retweetIcon.click()
		except ElementNotVisibleException:
			raise
		
		#click
		try:
			retweetbtn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.RetweetDialog-retweetActionLabel")))
		except TimeoutException:
			raise
		try: 
			retweetbtn.click()
		except ElementNotVisibleException:
			raise
	
		#click and done
