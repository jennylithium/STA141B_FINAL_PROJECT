#!/usr/bin/env python
# coding: utf-8

# In[152]:


import pandas as pd
import numpy as np
import plotnine as p9
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# In[200]:


sold = pd.read_csv('sold.csv', index_col = [0])
sold['price'] = sold['price'].str.replace('M','0000')
sold['price'] = sold['price'].str.replace('.','')
sold['price'] = (sold['price'].str.split()).apply(lambda x: float(x[0].replace('--', '0')))

sold = sold[(sold.T != 0).any()]
del sold['building_type']
sold.head()


# In[203]:


sold['price'].describe().astype('int64')


# The average listing price is $2,191,533, however, the median listing price is $1,299,000. The difference between the median and mean is so large becasue of listings found in 94123, the most expesnive area on average.   

# # Brokerage Listing Count

# In[184]:


fs_bk= sold['brokerage'].value_counts().rename_axis('brokerage').reset_index(name='counts')
fs_bk['brokerage'].replace({'0':'NO BROKERAGE REPORTED'}, inplace=True)
gg = p9.ggplot(fs_bk[:10])
gg += p9.aes(x='brokerage',y = 'counts', fill = 'brokerage')
#gg += p9.geom_histogram() 
gg += p9.geom_bar(stat = 'identity')
gg += p9.coord_flip()
gg += p9.labs(y='Counts of the Brokerages', x='Brokerage', title='Counts of the Brokerages')
gg


# In this bar graph, we are only looking at the ten most successful brokerages. Compass is by far the most dominant brokerage in San Francisco. At about 3 times less than the number of Compass listings, Vangaurd Properties and Sotheby's International Realty come in at second and third. 

# # Average Listing Price By Brokerage

# In[207]:


brokerage_mean = sold.groupby('brokerage').price.mean().rename_axis('brokerage').reset_index(name='avg price') 
not_brokerage = ['0']
brokerage_mean = brokerage_mean[~brokerage_mean['brokerage'].isin(not_brokerage)]
brokerage_mean = brokerage_mean.sort_values(['avg price'], ascending = False)

#gg = p9.ggplot(brokerage_mean)
gg = p9.ggplot(brokerage_mean[:10])
gg += p9.aes(x='brokerage',y = 'avg price', fill = 'brokerage')
gg += p9.geom_bar(stat = 'identity') 
gg


# In[208]:


gg = p9.ggplot(brokerage_mean)
gg += p9.aes(x='brokerage',y = 'avg price')
gg += p9.geom_bar(stat = 'identity') 
gg


# # Agent Listing Count

# In[209]:


fs_ag= sold['agent'].value_counts().rename_axis('agent').reset_index(name='counts')
fs_ag['agent'].replace({'0':'NO AGENT REPORTED'}, inplace=True)
not_agents = ['NO AGENT REPORTED', ' INC.', ' COMPASS', ' INC', ' POLARIS PACIFIC', ' BROKER']
fs_ag= fs_ag[~fs_ag['agent'].isin(not_agents)]
fs_ag
gg = p9.ggplot(fs_ag[:15])
gg += p9.aes(x='agent',y = 'counts', fill = 'agent')
gg += p9.geom_bar(stat = 'identity') 
gg += p9.coord_flip()
gg += p9.labs(y='Counts of the Agent', x='Agent', title='Counts of the Agent')
gg


# In[210]:


gg = p9.ggplot(fs_ag)
gg += p9.aes(x = 'counts')
gg += p9.geom_histogram(bins=20) 
gg


# In[211]:


sold.dtypes


# In[213]:


sns.heatmap(heat.corr(), vmax=.8, linewidths=0.01,
            square=True,annot=True,cmap='viridis',linecolor="white")
plt.title('Correlation Between Features')


# # Linear Regression on Price and Square Feet

# In[214]:


sold['price'] = sold['price'].astype(float)
sold['sqft'] = sold['sqft'].astype(float)

length = len(sold['price'])
x = sold[['sqft']]
y = sold[['price']]
reg = LinearRegression()
reg.fit(x,y)

plt.scatter(x, y,  color='grey', alpha =0.2)
plt.plot(x, reg.predict(x), color='red', linewidth=2)
plt.title('Price vs Square Feet')
plt.xlabel('Square Feet')
plt.ylabel('Price')
plt.show()


# # Price vs Zip

# In[215]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='zip',
                          y='price', color='zip'))
    + p9.geom_boxplot()
  + p9.labs(title="Price vs Zip")
)


# # Price by # of Baths 

# In[218]:


(p9.ggplot(data=build_comp,
          mapping=p9.aes(x='baths',
                          y='price', color='baths'))
    + p9.geom_boxplot()
 + p9.labs(title="Price by # of Baths")
)


# # Price By # of Beds

# In[219]:


build_comp['beds']
(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='beds',
                          y='price', color='beds'))
    + p9.geom_boxplot()
 + p9.labs(title="Price by # of Beds")
)


# # Price vs Square Feet By Area Code

# In[221]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='sqft',
                          y='price',
                          color='zip'))
    + p9.geom_point(alpha=0.5)
 + p9.labs(title="Price vs Square Feet By Area Code")
)

