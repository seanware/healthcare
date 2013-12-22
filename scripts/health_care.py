#Access the twitter stream and search for references to the Affordable
#care act.

import twitter
import json
import pymongo


def oauth_login():
	""" Use the twitter ouath credentials to create and instance of the 
	twitter api"""
	
	CONSUMER_KEY = 'eVrfLTLytTGB9bg6sUVRQ'
	CONSUMER_SECRET = 'XqxFx2SXq4zEaSVdlSBPAhBIJwa3PNoew5ezsi1dUAo'
	OAUTH_TOKEN = '1401308084-XkdSE7QSHtsnFntsxpyr6OJwnScvKtEYEHVxKmQ'
	OAUTH_TOKEN_SECRET = 'DLUpOCVBnXFdnzuzqQHaPh1M4XWmDUYCkf0ImN1qzoa1X'
	
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
						CONSUMER_KEY, CONSUMER_SECRET)
						
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api
	
	
def twitter_search(twitter_api, q, max_results = 200, **kw):
	""" Functions to search and return tweets modified from mining the
	social web"""
	
	search_results = twitter_api.search.tweets(q=q, count=100, **kw)
	
	statuses = search_results['statuses'] #return the body of the request
	
	max_results = min(1000, max_results) #Keep results less than 1000 tweets
	
	for _ in range(10):
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e:
			break
			
		#create a dictionary containing the tweets
		#previously text is ?max_id=13290409328472&q=QUERY&include_entities=1
		kwargs = dict([kv.split('=') for kv in next_results[1:].split('&')])
		
		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']
		
		if len(statuses) > max_results:
			break
			
	return statuses
				

def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
	"""
	Gives the option to save tweets to a mongo database
	"""
	
	client = pymongo.MongoClient(**mongo_conn_kw)
	
	db = client[mongo_db]
	
	coll = db[mongo_db_coll]
	
	return coll.insert(data)
	
	
def get_text(statuses):	
	return  [statuses[tweet]['text'] for tweet in xrange(len(statuses))]
		
		
def get_screen_names(statuses):	
	return [user_mention['screen_name'] for status in statuses 
			for user_mention in status['entities']['user_mentions']]
	
def get_hashtags(statuses):
	return [hashtag['text'] for status in statuses
			for hashtag in status['entities']['hashtags']]
			
def get_urls(statuses):
	return [url['expanded_url'] for status in statuses
			for url in status['entities']['urls']]
	
			
def show_list(tweets_list):
	#helper function to print the contents of list to stdout
	for tweet in tweets_list:
		print tweet.encode('utf-8')
		

def tweet_stream(query_list):
	"""
	Acess twitters 1% firehouse and loads prints data 
	that matches a tweet.
	"""
	twitter_api = oauth_login()
	twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
	stream = twitter_stream.statuses.filter(track=query_list)
	
	for tweet in stream:
		print tweet
		


	
	
	
if __name__=="__main__":
	twitter_api = oauth_login()
	q ='affordablecareact'
	results = twitter_search(twitter_api,q, max_results = 1000)
	show_list(get_screen_names(results))

	
		