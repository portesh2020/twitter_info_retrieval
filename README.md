
## Authors
Hannah Portes

## Files
Name | Purpose
--- | ---
`main.py` | This is the main script that calls on the Twitter class and interacts with the user
`Twitter.py` | This class contains all the code for interacting with the twitter API
`.env` | This is the environment file that contains the api keys required for interacting with Google and Twitter

## Program Run Instructions
In the root of the project directory run the following command:
```
$ python3 main.py
```
The user will be prompted to enter an email and then a username of interest. The email is a required field and cannot be left blank, while the name is optional

## Architecture
The program begins by saving the email and optional name provided by the user. A query is then constructed containing the email, name, and specifying the site as ```site:twitter.com``` to see if there is a twitter account that comes up related to these inputs. If there is no account found the program ends and prints out a message. 

If an account is found, the program then gets the user id, username, and name registered to the account by querying the Twitter api using ```get_user_info```. Once the program has the id of the user and the username, some other information is collected to be returned as final output.

## Additional Methods
#### get_sorted_tweets()
- This method retrieves 100 tweets associated with the located users account and pulls the public metrics for calculations. The number of retweets and likes are tallied, and the 100 tweets are then sorted in descending order of this total. The final number of likes and retweets, along with the text of these tweets are put into the final output json.

#### get_mentions()
- This method retrieves at most 15 tweets mentioning the identified user.

#### get_user_stats()
- This method is responsible for getting the public metrics of an individual account. The user id identified is passed to Twitter and the number of followers, number of users this account is following, and the number of tweets corresponding to this user are collected.

#### return_all_info()
- This method calls all the other methods in the Twitter class and organizes the information to be output as a final json.

## Notes
- .env directory location is hardcoded, if the program should look elsewhere for environment variables this must be changed in Twitter.py and main.py
- The environment variable names are hardcoded, I've included an example .env file for ease of running.