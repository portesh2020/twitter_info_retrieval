
import tweepy 
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import pprint

class Twitter:
    
    def __init__(self, username):
        """
        .env file to set envirionment variables for twitter api
        
        args
            username: string, twitter username
        """
        dotenv_path = Path('./.env')
        load_dotenv(dotenv_path=dotenv_path)
        api_key = os.getenv('APIKEY')
        api_secret = os.getenv('APISECRET')
        bearer_token = os.getenv('BEARERTOKEN')
        access_token = os.getenv('ACCESSSTOKEN')
        access_secret = os.getenv('ACCESSSECRET')
        
        if api_key and api_secret and bearer_token and access_token and access_secret:
            print('Loaded all variables successfully')
        else:  
            if not api_key:
                print('Error loading APIKEY')
            if not api_secret:
                print('Error loading APISECRET')
            if not bearer_token:
                print('Error loading BEARERTOKEN')
            if not access_secret:
                print('Error loading ACCESSSSECRET')
            if not access_token:
                print('Error loading ACCESSSTOKEN')
            raise Exception('Error with env variables')
        
        self.client = tweepy.Client( bearer_token=bearer_token, 
                                consumer_key=api_key, 
                                consumer_secret=api_secret, 
                                access_token=access_token, 
                                access_token_secret=access_secret, 
                                return_type = requests.Response,
                                wait_on_rate_limit=True)
        self.json = {}
        self.username = str(username)

    def get_user_info(self):
        """
        Get user information (username, name, id) from the username found in main.py
        sample response json 
            {'data': 
              {'id': '12345678', 
              'name': 'Hannah Portes', 
              'username': 'mangosmom'}
            }
        """
        print('Getting user information...')
        client = self.client
        response = client.get_user(username=self.username)
        if response.status_code == 200:    
            response = response.json()['data']
            twitter_id = response['id']
            twitter_name = response['name']
            twitter_username = response['username']
            
            self.username = twitter_username
            self.user_id = twitter_id
            return twitter_id, twitter_name, twitter_username
        else:
            print('Error calling Twitter API')
            return None
        
    def get_sorted_tweets(self, twitter_id, max_results=100):
        """
        This function gets 100 tweets and sorts them by likes and retweet count to
        find the top and bottom tweets
        
        args
            twitter_id: int, integer corresponding to a single twitter user
            max_results: int, maximum number of results returned by the API
        """
        client = self.client
        tweets = client.get_users_tweets(twitter_id, tweet_fields=["public_metrics"], max_results=max_results, expansions=["author_id"])
        tweets = tweets.json()['data']
        # sort tweets by popularity of retweet count + like count
        tweets.sort(key=lambda t: t['public_metrics']["retweet_count"] + t['public_metrics']["like_count"], reverse=True)
        # get the information of the most and least popular tweets
        top_id = tweets[0]['id']
        top_text = tweets[0]['text']
        top_retweets = tweets[0]['public_metrics']['retweet_count']
        top_likes = tweets[0]['public_metrics']['like_count']
        bottom_id = tweets[-1]['id']
        bottom_text = tweets[-1]['text']
        bottom_retweets = tweets[-1]['public_metrics']['retweet_count']
        bottom_likes = tweets[-1]['public_metrics']['like_count']
        return [(top_id, top_text, top_retweets, top_likes), (bottom_id, bottom_text, bottom_retweets, bottom_likes)]
    
    def get_mentions(self, max_results=15):
        """
        Get mentions of a user
        
        args
            max_results: int, max results returned by the API
        """
        client = self.client
        response = client.get_users_mentions(self.user_id, max_results=max_results).json()
        return response['data']
    
    def get_user_stats(self, id):
        """
        Get the user statistics
        """
        client = self.client
        response = client.get_user(id=id, user_fields='public_metrics').json()['data']['public_metrics']
        followers = response['followers_count']
        following = response['following_count']
        tweet_count = response['tweet_count']
        return followers, following, tweet_count
            
    def return_all_info(self):
        """ 
        This function aggregates all the data collected by the above calls to the API
        """
        twitter_id, twitter_name, twitter_username = self.get_user_info()
        followers, following, tweet_count = self.get_user_stats(twitter_id)
        self.json['Full Name'] = twitter_name
        self.json['Username'] = twitter_username
        self.json['Number of Followers'] = followers
        self.json['Number of Users Following'] = following
        self.json['Number of Tweets'] = tweet_count
        sorted_tweets = self.get_sorted_tweets(twitter_id)
        tweet_id, text, retweets, likes = sorted_tweets[0]
        bottom_id, bottom_text, bottom_retweets, bottom_likes = sorted_tweets[1]
        if not tweet_id:
            print('No popular tweets found')
        else:
            self.json['Most Popular Tweet'] = {'text': text, 'retweets': retweets, 'likes': likes}
        if not bottom_id:
            print('Bottom tweet not found')
        else:
            self.json['Least Popular Tweet'] = {'text': bottom_text, 'retweets': bottom_retweets, 'bottom_likes': bottom_likes}
        mentions = self.get_mentions()
        mentioned_list = []
        # add the tweets user was mentioned in to a list for final output
        for mention in mentions:
            mentioned_list.append(mention['text'])
        self.json['Tweets Mentioning User'] = mentioned_list
        return self.json