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
		
		win_for_me(bot, webdriver, "#FreebieFriday", 50)
		#win_for_me(bot, webdriver, "RT to WIN", 5)
		#win_for_me(bot, webdriver, "#FreebieFriday OR #giveaway", 5)


def win_for_me(bot, webdriver, searchquery, contestcount):

	#get contest_tweets
	statuses = bot.search(query=searchquery, lang='en', count=contestcount)

	#[]Statuses

	#createParsedTweets
	#[]ParsedTweet
	parsed_tweets = statuses_to_parsedTweets(statuses)

	#determine who NOT to follow
	already_following = get_already_following(bot, parsed_tweets)

	#now need to filter out the ones im already following.
	parsed_tweets = filter_already_following(parsed_tweets, already_following)

	for parsed_tweet in parsed_tweets:

		try:
			webdriver.follow_and_retweet_from_parsedTweet(parsed_tweet)
		except TimeoutException as e:
			print("contest_tweet: {0} failed with exception: {1}".format(parsed_tweet, e))
			continue
		except ElementNotVisibleException as e:
			print("contest_tweet: {0} failed with exception: {1}".format(parsed_tweet, e))
			continue

		continue

#[]Tweepy.Status -> []Classes.ParsedTweet
#filters out already retweeted ones
def statuses_to_parsedTweets(statuses):
	parsed_tweets = []
	for contest_tweet in statuses:
		if not contest_tweet.retweeted:
			author = determine_author(contest_tweet)
			mentions = determine_mentions(contest_tweet)
			tweet_id = determine_id(contest_tweet)

			parsed_tweets.append(ParsedTweet(tweet_id, author, mentions))

	return parsed_tweets

#Tweepy.Status -> string
def determine_author(contest_tweet):
	if hasattr(contest_tweet, 'retweeted_status'):
		return contest_tweet.retweeted_status.author.screen_name
		
	return contest_tweet.author.screen_name

#Tweepy.Status -> []string
def determine_mentions(contest_tweet):
	mentions = []

	if hasattr(contest_tweet, 'retweeted_status'):
		user_mentions = contest_tweet.retweeted_status.entities['user_mentions']
	else:
		user_mentions = contest_tweet.entities['user_mentions']

	if len(user_mentions) > 0:
			for i, val in enumerate(user_mentions):
				if not val['screen_name'] in mentions:
					mentions.append(val['screen_name'])

	return mentions

#Tweepy.Status -> int
def determine_id(contest_tweet):
	if hasattr(contest_tweet, 'retweeted_status'):			
			return contest_tweet.retweeted_status.id
			
	return contest_tweet.id

#[]Classes.ParsedTweet -> []string
def get_already_following(bot, parsed_tweets):
	people_to_check = []
	for parsed_tweet in parsed_tweets:
		people_to_check.append(parsed_tweet.author)
		people_to_check.extend(parsed_tweet.mentions)
	
	relationships = bot.check_relationship(people_to_check)
	
	already_following = []
	for relationship in relationships:
		if relationship.is_following:
			already_following.append(relationship.screen_name)

	return already_following

#[]Classes.ParsedTweet -> []Classes.ParsedTweet
def filter_already_following(parsed_tweets, already_following):
	#for each ParsedTweet, flag to follow the author, and save
	#metions that arent already being followed.
	for parsed_tweet in parsed_tweets:
		if parsed_tweet.author in already_following:
			parsed_tweet.follow_author = False

		new_mentions = []
		for mention in parsed_tweet.mentions:
			if mention not in already_following:
				new_mentions.append(mention)
		parsed_tweet.mentions = new_mentions

	return parsed_tweets
			
main()




	

		



