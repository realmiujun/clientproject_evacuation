#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import gmaps
with open ("C:/Users/yingr/Documents/IngridWang/IngridWang/GA/apik.txt", "r") as myfile:
    api_key = myfile.read().replace('\n', '')
    
#####################################################################
# Get last 24 hours traffic data from social media tweets, KCSBTraffic
#####################################################################

import GetOldTweets3 as got
import pandas as pd
import requests
from datetime import date,timedelta
import pickle
import regex as re
loaded_model = pickle.load(open('predictor.sav', 'rb'))
today = date.today()
yesterday = today - timedelta(days = 1)
to_df = []
accounts = ['KCBSAMFMTraffic']
exchange = {'SB':'southbound', 'NB':'northbound','EB':'eastbound','WB':'westbound',
           'Waze':'','WAZE':'','KCSBTraffic':'','KCBSTraffic':''}
def words_only(x):
    x = re.sub("[^a-zA-Z0-9]", " ", x)
    return ' '.join([exchange.get(word,word) for word in x.split()])
def tweets_to_df(twit):    
    #'TrafficOn17','CaltransD5','Cruz_511','FireDispatchSC'
    tweetCriteria = got.manager.TweetCriteria().setUsername(twit)                                       .setSince(str(yesterday))                                       .setUntil(str(today))
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    for i in range(len(tweet)):
        toappend = {}
        toappend['date'] = tweet[i].formatted_date
        toappend['id'] = tweet[i].author_id
        toappend['tweet'] = tweet[i].text
        to_df.append(toappend)
def search_sc():
    tweetCriteria = got.manager.TweetCriteria().setNear('San Francisco, California')                                       .setQuerySearch('road')                                       .setSince(str(yesterday))                                       .setUntil(str(today))                                       .setWithin('25mi')                                       .setMaxTweets(-1)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    for i in range(len(tweet)):
        toappend = {}
        toappend['date'] = tweet[i].formatted_date
        toappend['id'] = tweet[i].author_id
        toappend['tweet'] = tweet[i].text
        to_df.append(toappend)
for account in accounts:
    tweets_to_df(account)
search_sc()
df = pd.DataFrame(to_df)
df['closed'] = loaded_model.predict(df['tweet'])
df = df[df['closed']==1]
df['tweet'] = df['tweet'].map(words_only)    
df.to_csv('./datasets/last24hr_tweets.csv')

def get_lat_lng(df, api_key):
    for i, row in df.iterrows():
        row_text = row['tweet'] 
        temp_place = []
        rowlength = len(row_text.split())
        for j in range(rowlength):
            if j < (rowlength-1):
                temp_place.append(row_text.split()[j]+'%20')
            else:
                temp_place.append(row_text.split()[j])
        #print('temp_place :   ', temp_place)
        place = ''.join(temp_place)
        #print( 'place    :     '     ,place)
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place}&inputtype=textquery&fields=geometry&key='+api_key
        #print(url)
        res = requests.get(url)
        result = res.json()
        #print('result :    ', result) 
        #print('lat :   ', lat, 'lng :   ',lng)
        #print('result.status  :   ', result['status'])
        if (result['status']) == 'OK' :
            #print('OK')
            lat=result['candidates'][0]['geometry']['location']['lat']
            #print('lat   :  ', lat)
            df.loc[i,'latitude']=result['candidates'][0]['geometry']['location']['lat']  
            df.loc[i,'longitude']=result['candidates'][0]['geometry']['location']['lng']
            #print('df lng :  ',df.loc[i,'latitude'], df.loc[i,'longitude'])
        else:
            df.loc[i,'latitude']=(np.nan)
            df.loc[i,'longitude']=(np.nan)
    return df

########################################################################
# Get Coordinates from Tweets related to Traffic
# and then display to map
########################################################################
#df=pd.read_csv('./datasets/last24hr_tweets.csv')
df = get_lat_lng(df, api_key)
pd.set_option('display.max_colwidth',-1)

df_no_na = df.dropna()
df_no_na.to_csv('./datasets/tweet_geo_to_map.csv')
gmaps.configure(api_key)
fig = gmaps.figure()
#fig = gmaps.figure(center=locations, zoom_level=13, map_type='ROADMAP')
locations = df_no_na[['latitude','longitude']]
info_box = []
for i, row in df_no_na.iterrows():
    row_text = row['tweet'] 
    #print(row_text)
    info_box.append(row_text)
markers = gmaps.marker_layer(locations,info_box_content=info_box)
fig.add_layer(markers)
fig    


# In[ ]:




