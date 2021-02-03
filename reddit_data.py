import pandas as pd
import praw
from config import r_cid, r_csec, r_uag



def get_reddit(cid= r_cid, csec= r_csec, uag= r_uag, subreddit='wallstreetbets'):
    '''
    The function imports the dependencies and the API key from the config.py file, 
    then transform the data into a data frame
    '''
    #connect to reddit
    reddit = praw.Reddit(client_id= cid, client_secret= csec, user_agent= uag, check_for_async = False)
    #get the new reddit posts
    posts = reddit.subreddit(subreddit).new(limit=None)
    #load the posts into a pandas dataframe
    p = []
    for post in posts:
        p.append([post.title, post.score, post.selftext])
    posts_df = pd.DataFrame(p,columns=['title', 'score', 'post'])
    
    return posts_df