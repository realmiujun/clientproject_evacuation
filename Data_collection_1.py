#!/usr/bin/env python
# coding: utf-8

# In[1]:


import GetOldTweets3 as got
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import pickle
from datetime import date,timedelta


# ### Tweet sweep

# In[3]:


to_df = []
tweetCriteria = got.manager.TweetCriteria().setUsername('KCBSAMFMTraffic')                                       .setSince('2019-01-01')                                       .setUntil('2020-01-01')                                       .setMaxTweets(5000)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)
for i in range(len(tweet)):
    toappend = {}
    toappend['date'] = tweet[i].formatted_date
    toappend['id'] = tweet[i].author_id
    toappend['tweet'] = tweet[i].text
    to_df.append(toappend)
    
df = pd.DataFrame(to_df)
df.to_csv('./data/kcbsamfmtraffic.csv',index=False)


# ### Not so clean tweets

# In[19]:


to_df = []
accounts = ['TrafficOn17','CaltransD5','Cruz_511','FireDispatchSC']
def tweets_to_df(twit):    
    #'TrafficOn17','CaltransD5','Cruz_511','FireDispatchSC'
    tweetCriteria = got.manager.TweetCriteria().setUsername(twit)                                           .setSince("2019-01-01")                                           .setUntil("2020-01-01")
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    for i in range(len(tweet)):
        toappend = {}
        toappend['date'] = tweet[i].formatted_date
        toappend['id'] = tweet[i].author_id
        toappend['tweet'] = tweet[i].text
        to_df.append(toappend)
        
for account in accounts:
    to_df = []
    pd.DataFrame(tweets_to_df(account)).to_csv('./data/'+account+'.csv',index=False)
    time.sleep(3600)


# In[ ]:




