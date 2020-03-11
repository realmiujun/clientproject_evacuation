#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import gmaps

with open ("C:/Users/yingr/Documents/IngridWang/IngridWang/GA/apik.txt", "r") as myfile:
    api_key = myfile.read().replace('\n', '')

addr_from = '1156 High St, Santa Cruz, CA 95064'
addr_to = '710 Front St, Santa Cruz, CA 95060'
addr_f = addr_from.replace(' ','+')
addr_t = addr_to.replace(' ','+')

addr_f = addr_from.replace(' ','%20')

url_f = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={addr_f}&inputtype=textquery&fields=geometry&key='+api_key
res_f = requests.get(url_f)
result_f = res_f.json()
loc_from=result_f['candidates'][0]['geometry']['location']['lat'],result_f['candidates'][0]['geometry']['location']['lng']


url_f = f'https://maps.googleapis.com/maps/api/geocode/json?address={addr_f}&key={api_key}'
url_t = f'https://maps.googleapis.com/maps/api/geocode/json?address={addr_t}&key={api_key}'

res_f = requests.get(url_f)
result_f = res_f.json()
res_t = requests.get(url_t)
result_t = res_t.json()

loc_from = (result_f['results'][0]['geometry']['location']['lat'],result_f['results'][0]['geometry']['location']['lng'])
loc_to = (result_t['results'][0]['geometry']['location']['lat'],result_t['results'][0]['geometry']['location']['lng'])

gmaps.configure(api_key)
fig = gmaps.figure()
loc_from2loc_to = gmaps.directions_layer(loc_from, loc_to)
fig.add_layer(loc_from2loc_to)
fig

