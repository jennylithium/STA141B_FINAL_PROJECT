#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as soup
from collections import Counter
import lxml
import pandas as pd

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
from time import sleep 


# In[10]:


def process_zillset(html):
    """
    This function processes the zillow html for the differnt urls and returns the items of interest
    """
    for home in html:
        home.prettify()
        home.name, home.attrs, home['class']

        #address
        try:
            zaddress = home.find_all('address')
            address = zaddress[0].text.strip()
            zill_dict['address'].append(address)
        except IndexError:
            zill_dict['address'].append('NaN')
            
        
        #listing brokerage and agent 
        try:
            zlisting = home.find_all('p', {'class':'list-card-extra-info'})
            listingby = zlisting[0].text.strip()
            zill_dict['listingby'].append(listingby)
        except IndexError:
            zill_dict['listingby'].append('NaN')
            
        
        #price
        try:
            zprice = home.find_all('div', {'class':'list-card-price'})
            price = zprice[0].text.strip()
            zill_dict['price'].append(price)
        except IndexError:
            zill_dict['price'].append('NaN')
            
        
        #beds
        try:
            zbed = home.find_all('li', {'class':''})
            beds = zbed[0].text.strip()
            zill_dict['beds'].append(beds)
        except IndexError:
            zill_dict['beds'].append('NaN')
            
        
        #bathrooms
        try:
            zbath = home.find_all('li', {'class':''})
            baths = zbath[1].text.strip()
            zill_dict['baths'].append(baths)
        except IndexError:
            zill_dict['baths'].append('NaN')
            
        
        #sqft
        try:
            zsqft = home.find_all('li', {'class':''})
            sqft = zsqft[2].text.strip()
            zill_dict['sqft'].append(sqft)
        except IndexError:
            zill_dict['sqft'].append('NaN')
            
            
        #type
        try:
            ztype = home.find_all('li', {'class':'list-card-statusText'})
            types = ztype[0].text.strip()
            zill_dict['building_type'].append(types)
        except IndexError:
            zill_dict['building_type'].append('NaN')
            
    return zill_dict
    


# In[27]:


# make _urls returns a list of Zillow urls, incrementing the page number until it reaches the max_page 
def make_urls(max_page):
    url_list =[]
    for pageNumber in range(1,max_page+1):
        #url = 'https://www.zillow.com/san-francisco-ca/' + str(pageNumber) + '_p?'
        url = 'https://www.zillow.com/san-francisco-ca/rentals/'+ str(pageNumber) + '_p?'
        url_list += [url]
    return url_list 


# In[41]:


# we give the max_page and call make_urls to make a list of urls that we will use 
max_page = 20
zillow_urls = make_urls(max_page)
print(zillow_urls)


# In[42]:


zill_dict = {'address':[], 'listingby':[], 'price':[],'beds':[], 'baths':[],'sqft':[], 'building_type':[], 'price/sqft':[]}
for url in zillow_urls:
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome()
    page = driver.get(url)
    #time.sleep(10)
    zillhtml= driver.page_source

    #making into soup object
    zill = soup(zillhtml,'html.parser') 
    zill_content = zill.find_all('div', attrs ={'class':'list-card-info'})
    print(url)
    zill_count = 1
    for zills in zill_content:
        zill_count+=1
    dict=process_zillset(zill_content)
    df = pd.DataFrame.from_dict(dict, orient='index').transpose()


# In[43]:


df


# In[44]:


df['address'].value_counts()

