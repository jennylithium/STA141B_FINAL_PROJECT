#!/usr/bin/env python
# coding: utf-8

# In[58]:


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


# In[ ]:


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
    


# In[59]:


# make _urls returns a list of Zillow urls, incrementing the page number until it reaches the max_page 
def make_urls(max_page):
    url_list =[]
    for pageNumber in range(1,max_page+1):
        #url = 'https://www.zillow.com/san-francisco-ca/' + str(pageNumber) + '_p?'
        url = 'https://www.zillow.com/san-francisco-ca/rentals/'+ str(pageNumber) + '_p?'
        url_list += [url]
    return url_list 


# In[89]:


# we give the max_page and call make_urls to make a list of urls that we will use 
max_page = 2
zillow_urls = make_urls(max_page)
print(zillow_urls)


# In[ ]:


zill_dict = {'address':[], 'listingby':[], 'price':[],'beds':[], 'baths':[],'sqft':[], 'building_type':[], 'price/sqft':[]}
for url in zillow_urls:

    driver = webdriver.Chrome()
    page = driver.get(url)
    time.sleep(20)
    zillhtml= driver.page_source

    #making into soup object
    zill = soup(zillhtml,'lxml') 
    zill_content = zill.find_all('div', attrs ={'class':'list-card-info'})
    print(url)
    zill_count = 1
    for zills in zill_content:
        zill_count+=1
    dict=process_zillset(zill_content)
    df = pd.DataFrame.from_dict(dict, orient='index').transpose()


# In[230]:


zillow_fs = pd.read_csv("ZillowData.csv", index_col=[0])

zillow_fs.shape


# In[196]:


# removing unwanted parts in column values
zillow_fs['sqft'] = zillow_fs['sqft'].str.rstrip('sqft')
zillow_fs['sqft'] = zillow_fs['sqft'].str.replace(',', '')
zillow_fs['sqft'] = zillow_fs['sqft'].str.replace('--', '0')
zillow_fs['baths']= zillow_fs['baths'].str.rstrip('ba')
zillow_fs['beds'] = zillow_fs['beds'].str.rstrip('bds')
zillow_fs['price'] = zillow_fs['price'].str.replace('$', '')
zillow_fs['price'] = zillow_fs['price'].str.replace(',', '')
zillow_fs['price'] = zillow_fs['price'].str.rstrip('+')


# In[197]:


# splitting up string values in columns
zillow_fs['zip']= zillow_fs['address'].str.split().str[-1]
zillow_fs['address'] = zillow_fs['address'].str.split(',',expand =True)[0]
zillow_fs['agent'] = zillow_fs['listingby'].str.split(',', expand=True)[1]
zillow_fs['brokerage'] = zillow_fs['listingby'].str.split(',', expand=True)[0]
zillow_fs = zillow_fs.drop(columns =['listingby'])


# In[200]:


# dividing price and sqft column to create price per sqft
zillow_fs=zillow_fs.fillna(0)
zillow_fs[['price', 'sqft']] = zillow_fs[['price', 'sqft']].apply(pd.to_numeric)
zillow_fs['price/sqft'] = zillow_fs['price'].astype(int) / zillow_fs['sqft'].astype(int)


# In[227]:


zillow_fs = zillow_fs[['address', 'zip', 'building_type', 'price', 'beds', 'baths', 'sqft', 'price/sqft', 'agent', 'brokerage']]
zillow_fs.head()


# In[226]:


zillow_fs['brokerage'].value_counts()


# In[219]:


zillow_fs.to_csv('for_sale.csv')


# In[221]:


zillow_fr = pd.read_csv("ZillowRent.csv", index_col=[0])
zillow_fr.head()


# In[225]:


#zillow_fr['brokerage'].value_counts()


# In[216]:


# removing unwanted string parts in column
zillow_fr = zillow_fr.drop(columns =['listingby'])
zillow_fr = zillow_fr.rename(columns={'price':'rent/month'}, inplace=True)
zillow_fr['price'] = zillow_fr['price'].str.replace('$', '')
zillow_fr['price'] = zillow_fr['price'].str.replace(',', '')
zillow_fr['price'] = zillow_fr['price'].str.replace('/mo', '')
zillow_fr['beds'] = zillow_fr['beds'].str.rstrip('bds')
zillow_fr['beds'] = zillow_fr['beds'].str.rstrip('bd')
zillow_fr['baths'] = zillow_fr['baths'].str.rstrip('ba')
zillow_fr['sqft'] = zillow_fr['sqft'].str.rstrip('sqft')
zillow_fr['sqft'] = zillow_fr['sqft'].str.replace(',', '')
zillow_fr


# In[ ]:


zi

