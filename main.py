import requests
from Twitter import Twitter 
import os
from dotenv import load_dotenv
from pathlib import Path
import logging
import pprint


def prompt_user():
    """
    Function controlling the prompts for the user to enter 
    """
    email = input("Enter the email address of the person you would like me to locate on Twitter: ")
    if not email:
        print("A user email is required, please enter a user email.")
        prompt_user()
    name = input("If you would like, enter the name of the person you would like me to locate on Twitter, otherwise hit enter: ")
    query = email + " site:twitter.com"
    if name:
        query = name + ' ' + query 
    return query, email
        
def main():
    """
    The main function constructs a query containing the email, name, and specifying the site as
    site:twitter.com to see if there is a twitter account that. 
    
    If there is no account found the program ends, if an account is found, the program then gets 
    the user id, username, and name registered to the account by querying the Twitter API in Twitter.py
    """
    logging.basicConfig(filename='twitter.log', level=logging.ERROR)
    # set environment variables
    dotenv_path = Path('./.env')
    load_dotenv(dotenv_path=dotenv_path)    
    googleapi_key = os.getenv('GOOGLEAPI')
    cx = os.getenv('CX')
    
    if googleapi_key and cx:
        print('Loaded all variables successfully')
    else:  
        if not googleapi_key:
            print('Error loading GOOGLEAPIKEY')
        if not cx:
            print('Error loading CX')
        raise Exception('Error with env variables')

    query, email = prompt_user()
    print('Searching for Twitter user corresponding to: ', email)
    # gather information necessary to search google 
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": googleapi_key, "cx": cx, "q": query, "num": 1}
    response = requests.get(url, params=params)
    username = ''
    # parse the response to extract the located username 
    if response.status_code == 200:
        try:
            items = response.json()["items"]
            link = items[0]["link"]
            username = link.split("/")[-1]
            print(f"Found Twitter account: {username}")
        except:
            # no twitter account was returned by google API
            raise Exception(f"Error finding Twitter account, none found.")
    else:
        raise Exception(f"Error searching for Twitter account: {response.text}")
        
    if username:
    # get user information
        twitter = Twitter(username)
        json = twitter.return_all_info()
        pprint.pprint(json)
        return json

if __name__ == "__main__":
    main()
