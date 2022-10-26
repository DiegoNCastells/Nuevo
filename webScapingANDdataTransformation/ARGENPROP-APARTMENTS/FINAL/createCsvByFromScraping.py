#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import requests
from bs4 import BeautifulSoup as bs


# In[2]:


import lxml
import time


# In[3]:


LINK=[]


# In[4]:


url='https://www.argenprop.com/inmuebles-venta-barrio-palermo'
url_base='https://www.argenprop.com'
response = requests.get(url)


# In[5]:


if response.status_code == 200 :
    soup = bs(response.content,'html.parser')
    DimL = int( soup.find('li',attrs={'class':'pagination__page pagination__page--current'}).find('span').get_text())
    DimF = int( soup.find_all('li',attrs={'class':'pagination__page'})[4].get_text() )


# In[6]:


LINK.append(url)

#while(DimL<5):
while(DimL<DimF):

    try:
        sigLink = url_base + soup.find('li',attrs={'class':'pagination__page-next pagination__page'}).find('a').get('href')
        response = requests.get(sigLink)
        soup=bs(response.content,'html.parser')
        LINK.append(sigLink)
    except:
        print('error')
    DimL=DimL+1
print(LINK)


# In[7]:


LINK


# In[8]:


aux=[]
for i in range(0,len(LINK )):
    aux.append(i)
data=zip(aux,LINK)


# In[9]:


def _save_cars(data_,name,csv_headers):
    import csv
    out_file_name = 'Argenprop_{x}.csv'.format(x=name)
    
    with open(out_file_name, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for data in data_:
            row =data 
            print(row)
            writer.writerow(row)


# In[10]:


csv_headers=['id','link']
name_csv='links'
_save_cars(data,name_csv,csv_headers)


# In[11]:


import pandas as pd
import numpy as np


# In[12]:


data=pd.read_csv('Argenprop_links.csv',encoding='utf-8')
data


# In[ ]:





# In[ ]:




