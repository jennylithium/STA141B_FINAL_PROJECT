#!/usr/bin/env python
# coding: utf-8

# In[294]:


import pandas as pd
import numpy as np
import plotnine as p9
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# In[73]:


for_sale = pd.read_csv('for_sale.csv', index_col = [0])
for_sale.head()


# In[ ]:


for_sale['price'].min()


# In[36]:


#for_sale.loc[for_sale['zip']=='94123']


# In[40]:


#for_sale[['beds', 'baths']].astype('int64')


# # Property Types

# In[12]:


fs_bt = for_sale['building_type'].value_counts().rename_axis('building_type').reset_index(name='counts')

gg = p9.ggplot(fs_bt)
gg += p9.aes(x='building_type',y = 'counts', fill = 'building_type')
gg += p9.geom_bar(stat = 'identity') 
gg


# The most common property type being sold is a condo, followed by houses and multi family homes for sale.

# # For Sale Listings By ZIP Code

# In[20]:


fs_zip = for_sale['zip'].value_counts().rename_axis('zip').reset_index(name='counts')
not_zip=['BMR', 'Serif', '555', 'Portola', 'OneEleven', 'MIRA', 'Monarch']
fs_zip = fs_zip[~fs_zip['zip'].isin(not_zip)]

gg = p9.ggplot(fs_zip)
gg += p9.aes(x='zip',y = 'counts', fill = 'zip')
gg += p9.geom_bar(stat = 'identity') 
gg


# From this graph, we can clearly see that some zip codes have more listings than other zip codes. The zip code with the highest amount of listings is 94110, which corresponds to the Mission District. 

# # Average Listing Price By ZIP Code

# In[21]:


zip_mean = for_sale.groupby('zip').price.mean().rename_axis('zip').reset_index(name='avg price') 
zip_mean = zip_mean[~zip_mean['zip'].isin(not_zip)]

gg = p9.ggplot(zip_mean)
gg += p9.aes(x='zip',y = 'avg price', fill = 'zip')
gg += p9.geom_bar(stat = 'identity') 
gg


# In[39]:


for_sale['price'].describe().astype('int64')


# The average listing price is $2,191,533, however, the median listing price is $1,299,000. The difference between the median and mean is so large becasue of listings found in 94123, the most expesnive area on average.   

# # Brokerage Listing Count

# In[214]:


fs_bk= for_sale['brokerage'].value_counts().rename_axis('brokerage').reset_index(name='counts')
fs_bk['brokerage'].replace({'0':'NO BROKERAGE REPORTED'}, inplace=True)
gg = p9.ggplot(fs_bk[:10])
gg += p9.aes(x='brokerage',y = 'counts', fill = 'brokerage')
#gg += p9.geom_histogram() 
gg += p9.geom_bar(stat = 'identity') 
gg


# In this bar graph, we are only looking at the ten most successful brokerages. Compass is by far the most dominant brokerage in San Francisco. At about 3 times less than the number of Compass listings, Vangaurd Properties and Sotheby's International Realty come in at second and third. 

# # Average Listing Price By Brokerage

# In[34]:


brokerage_mean = for_sale.groupby('brokerage').price.mean().rename_axis('brokerage').reset_index(name='avg price') 
not_brokerage = ['0']
brokerage_mean = brokerage_mean[~brokerage_mean['brokerage'].isin(not_brokerage)]
brokerage_mean = brokerage_mean.sort_values(['avg price'], ascending = False)

#gg = p9.ggplot(brokerage_mean)
gg = p9.ggplot(brokerage_mean[:10])
gg += p9.aes(x='brokerage',y = 'avg price', fill = 'brokerage')
gg += p9.geom_bar(stat = 'identity') 
gg


# In[ ]:


gg = p9.ggplot(brokerage_mean)
gg += p9.aes(x='brokerage',y = 'avg price')
gg += p9.geom_bar(stat = 'identity') 
gg


# # Agent Listing Count

# In[182]:


fs_ag= for_sale['agent'].value_counts().rename_axis('agent').reset_index(name='counts')
fs_ag['agent'].replace({'0':'NO AGENT REPORTED'}, inplace=True)
not_agents = ['NO AGENT REPORTED', ' INC.', ' COMPASS', ' INC', ' POLARIS PACIFIC', ' BROKER']
fs_ag= fs_ag[~fs_ag['agent'].isin(not_agents)]
fs_ag
gg = p9.ggplot(fs_ag[:15])
gg += p9.aes(x='agent',y = 'counts', fill = 'agent')
gg += p9.geom_bar(stat = 'identity') 
gg


# In[224]:


gg = p9.ggplot(fs_ag)
gg += p9.aes(x = 'counts')
gg += p9.geom_histogram(bins=20) 
gg


# In[72]:


for_sale.dtypes


# # Heat Map

# In[471]:


heat = for_sale[['zip', 'price', 'beds', 'baths', 'sqft', 'building_type']]

# not zips
heat = heat[~heat['zip'].isin(not_zip)]
# not beds
not_beds=['4,996 sqft lot', '1,470 sqft lot', '5.72 acres lot', '2,496 sqft lot','1.15 acres lot','2,788 sqft lot','--','Studio', '84 ']
heat = heat[~heat['beds'].isin(not_beds)]
# not baths
not_baths=['-- ']
heat = heat[~heat['baths'].isin(not_baths)]
# not sqft
not_sqft=['0']
heat = heat[~heat['sqft'].isin(not_sqft)]

build_comp = heat[['price','sqft', 'beds', 'baths' ,'zip', 'building_type']]

heat= heat[['price','sqft', 'beds', 'baths']].astype('int64')
#heat


# In[472]:


sns.heatmap(heat.corr(), vmax=.8, linewidths=0.01,
            square=True,annot=True,cmap='viridis',linecolor="white")
plt.title('Correlation Between Features')


# # Linear Regression on Price and Square Feet

# In[473]:


length = len(build_comp['price'])
x = build_comp[['sqft']]
y = build_comp[['price']]
reg = LinearRegression()
reg.fit(x,y)

plt.scatter(x, y,  color='grey', alpha =0.2)
plt.plot(x, reg.predict(x), color='red', linewidth=2)
plt.title('Price vs Square Feet')
plt.xlabel('Square Feet')
plt.ylabel('Price')
plt.show()


# # Price vs Zip

# In[474]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='zip',
                          y='price', color='zip'))
    + p9.geom_boxplot()
  + p9.labs(title="Price vs Zip")
)


# # Price By Building Type

# In[475]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='building_type',
                          y='price', color='building_type'))
    + p9.geom_boxplot()
    + p9.labs(title="Price By Building Type")
)


# # Square Feet By Building Type

# In[476]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='building_type',
                          y='sqft', color='building_type'))
    + p9.geom_boxplot()
 + p9.labs(title="Square Feet By Building Type")
)


# In[477]:


#build_comp.dtypes


# In[478]:


#build_comp = build_comp.astype({"beds": int, "baths": int, "zip": int})
#build_comp


# # Price by # of Baths 

# In[479]:


(p9.ggplot(data=build_comp,
          mapping=p9.aes(x='baths',
                          y='price', color='baths'))
    + p9.geom_boxplot()
 + p9.labs(title="Price by # of Baths")
)


# # Price By # of Beds

# In[480]:


build_comp['beds']
(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='beds',
                          y='price', color='beds'))
    + p9.geom_boxplot()
 + p9.labs(title="Price by # of Beds")
)


# # Price vs Square Feet By Building Type

# In[465]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='sqft',
                          y='price',
                          color='building_type'))
    + p9.geom_point(alpha=0.5)
 + p9.labs(title="Price vs Square Feet By Building Type")
)


# # Price vs Square Feet By Area Code

# In[466]:


(p9.ggplot(data=build_comp,
           mapping=p9.aes(x='sqft',
                          y='price',
                          color='zip'))
    + p9.geom_point(alpha=0.5)
 + p9.labs(title="Price vs Square Feet By Area Code")
)

