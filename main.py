from classes import *
import tweepy, os, datetime, time, random
from selenium.common.exceptions import *
#TimeoutException, NoSuchElementException, ElementNotVisibleException, StaleElementReferenceException


#botnumber should be 1, later will need to be a range
def make_bot():
	print('making bot')
	connection = APIKeys().connect()
	return Bot(connection)
def main():
	bot = make_bot()
	try:
		webdriver = Selenium()
		webdriver.login()
	except TimeoutException as e:
		print(e)

	while True:
		
		win_for_me(bot, webdriver, "#winitwednesday", 5)
		#win_for_me(bot, webdriver, "RT to WIN", 5)
		#win_for_me(bot, webdriver, "#FreebieFriday OR #giveaway", 5)


def get_selenium_instructions(bot, contest_tweet):
		print('started instructions')
	
		author = ''
		tweet_id = 0
		user_mentions = []
		#ensure we follow the original tweeter if this is not them.
		if hasattr(contest_tweet, 'retweeted_status'):
			author = contest_tweet.retweeted_status.author
			tweet_id = contest_tweet.retweeted_status.id
			user_mentions = contest_tweet.retweeted_status.entities['user_mentions']
		else:
			author = contest_tweet.author
			tweet_id = contest_tweet.id
			user_mentions = contest_tweet.entities['user_mentions']
		#user_mentions is a list of dicts [{}, {}], messy data structure if you ask me.
		##additional people to follow for the tweet, if any.
		##sometimes they be like, follow me and @thisguy to win yo.
		##initialize with the OT - original tweeter.
		people_to_follow = [author.screen_name]


		if len(user_mentions) > 0:
				for i, val in enumerate(user_mentions):
					if not val['screen_name'] in people_to_follow:
						people_to_follow.append(val['screen_name'])

		people_to_follow = bot.filter_already_following(people_to_follow)
					
		newSI = SeleniumIntructions(author.screen_name, people_to_follow, tweet_id)
		
		return newSI


def win_for_me(bot, webdriver, searchquery, contestcount):
	contests = bot.search(query=searchquery, lang='en', count=contestcount)

	for contest_tweet in contests:
		si = get_selenium_instructions(bot, contest_tweet)
		try:
			webdriver.follow_and_retweet(si)
		except TimeoutException as e:
			print("contest_tweet: {0} failed with exception: {1}".format(contest_tweet, e))
			continue
		except ElementNotVisibleException as e:
			print("contest_tweet: {0} failed with exception: {1}".format(contest_tweet, e))
			continue
main()




	

		



