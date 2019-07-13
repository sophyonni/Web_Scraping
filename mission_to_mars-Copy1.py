#!/usr/bin/env python
# coding: utf-8

# # Libraries

# In[27]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import pymongo
import os
import datetime as dt
from selenium import webdriver


# In[28]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[29]:


# database and collection
db = client.mars_mission_db
collection = db.items


# In[30]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[31]:


# mars_html = browser.html
# mars_nasa_data = BeautifulSoup(mars_html, 'html.parser')


# In[32]:


url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)    


# In[33]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())


# # Web scraping

# In[34]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[35]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# # NASA Mars News/Image

# In[36]:


news_title = soup.find('div', class_='content_title').text
print(news_title)


# In[37]:


news_p = soup.find('div', class_='article_teaser_body').text
print(news_p)


# In[38]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[39]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[40]:


# Image 
image = soup.find('footer').find('a', class_='button fancybox')['data-fancybox-href']
print(image)


# In[41]:


featured_image_url= 'https://www.jpl.nasa.gov'+image
print(featured_image_url)


# # Mars Weather

# In[42]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[43]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[44]:


soup.find('p', class_='tweet-text').text


# # Mars Facts

# In[45]:


# url = 'https://space-facts.com/mars/'
# browser.visit(url)


# In[46]:


# html = browser.html
# soup = BeautifulSoup(html, 'html.parser')


# In[47]:


# soup.find('span', class_= 'mars-s')


# In[48]:


# Read Mars Facts webpage; use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
mars_facts_url = 'https://space-facts.com/mars/'
mars_facts_table_df = pd.read_html(mars_facts_url)[0]
mars_facts_table_df.column = ['Description','Value']
mars_facts_table_df


# In[49]:


# Use Pandas to convert the data to a HTML table string and save to a file
mars_facts_table_df.to_html('MarsFactsTable.html', index=False )
mars_facts_table_df.to_html()


# In[50]:


# URL of USGS Astrogeology site to be scraped
# to obtain high resolution images for each of Mar's hemispheres
usgs_astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_astrogeology_url)

# Initialize the list for the dictionary of hemisphere images 
hemisphere_image_urls = []

# Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
usgs_astrogeology_html = browser.html
all_hemisphere_data = BeautifulSoup(usgs_astrogeology_html, 'html.parser')
all_hemisphere_data


# In[51]:


# Get the iterable list of all hemispere information
hemisphere_results = all_hemisphere_data.find('div', class_='collapsible results').find_all('div',class_='item')
hemisphere_results


# In[52]:


# Loop through hemisphere results
for each_hemisphere in hemisphere_results:
    
    # Get each hemisphere title 
    # hem_title = each_hemisphere.find('div', class_='description').h3.text
    hem_title = each_hemisphere.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
    ###print(hem_title)
    # Exclude the word 'Enhanced'
    short_hem_title = ' '.join(hem_title.split()[0:-1])
    ###print(short_hem_title)
     
    # Get each hemisphere image URL
    base_hem_url = 'https://astrogeology.usgs.gov'

    each_hem_image_url = base_hem_url + each_hemisphere.find('a',class_='itemLink product-item')['href']
    ###print(each_hem_image_url)
    
    browser.visit(each_hem_image_url)
    time.sleep(2)
    each_hem_img_html = browser.html
    each_hem_data = BeautifulSoup(each_hem_img_html, 'html.parser')
    full_image_url = each_hem_data.find('div',class_='downloads').a['href']
    ###print(full_image_url)
    
    each_hemisphere_image = {
        "title" : short_hem_title,
        "image_url" : full_image_url
    }
    print(each_hemisphere_image)
    # Append each hemisphere info to the list of all hemipheres  
    hemisphere_image_urls.append(each_hemisphere_image)


# In[53]:


print(hemisphere_image_urls)


# In[ ]:




