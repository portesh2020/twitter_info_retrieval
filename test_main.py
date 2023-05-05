import unittest
from Twitter import Twitter

class TestTwitter(unittest.TestCase):
    def test_get_user_info(self):
        """
        Test the function getting the user information when given the username taylorswift13
        """
        twitter = Twitter('taylorswift13')
        returned = twitter.get_user_info()
        expected_return = ('17919972', 'Taylor Swift', 'taylorswift13')
        self.assertEqual(returned, expected_return)
        
    def test_get_user_stats(self):
        """
        Test function getting user stats (followers, following, and tweet count)
        """
        twitter = Twitter('taylorswift13')
        id, name, username = twitter.get_user_info()
        followers, following, tweet_count = twitter.get_user_stats(id)
        # at the time of testing Taylor Swift has 92M followers, is following 0 accounts, and has tweets posted
        self.assertTrue(30000000 <= followers) 
        self.assertTrue(0 == following)
        self.assertTrue(50 <= tweet_count)
        
if __name__ == '__main__':
    unittest.main()
    
