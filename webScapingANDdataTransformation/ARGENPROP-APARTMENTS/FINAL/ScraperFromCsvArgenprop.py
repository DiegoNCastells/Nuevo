#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:


data=pd.read_csv('Argenprop_links.csv',encoding='utf-8') 


# In[ ]:


links=list(data['link'])


# In[ ]:


url_base='https://www.argenprop.com'


# In[ ]:


import re
import requests
from bs4 import BeautifulSoup as bs


# In[ ]:


def cleanData(price,expenses,direcction,coveredArea,bedrooms,antiquity,toilets,environments,garages,condition,provision):
    #price,expenses,direcction,coveredArea,bedrooms
    #antiquity,toilets,environments,garages,condition,provision
    currencyPurchase=price.split()[0]
    pricePurchase=price.split()[1]
    expensesCurrency=expenses.split()[1][0:1]
    expensesPrice=1000*expenses.split()[1][1:]
    coveredArea=coveredArea.split()[0]
    bedrooms=bedrooms.split()[0]
    antiquity=antiquity.split()[0]
    toilets=toilets.split()[0]
    environments=environments.split()[0]
    garages=garages.split()[0]
    return ( currencyPurchase,pricePurchase,expensesCurrency,expensesPrice,direcction,coveredArea,bedrooms,antiquity,toilets,environments,garages,condition,provision )


# In[ ]:


name_csv = 'betaArgenProp'


# In[ ]:


aparthments=[]

for link in links:
    response = requests.get(link)
    soup=bs(response.content,'html.parser')
    post=soup.find_all('a',attrs={'card'})
    aparthment=[ url_base + n.get('href') for n in post ] 
    aparthments.extend(list(aparthment))


# In[ ]:


#len(aparthments)
#aparthments


# In[ ]:


listaAparthment=[]
tot=0
error=0
for aparthment in aparthments:
    response = requests.get(aparthment)
    Aparthment=bs(response.content,'html.parser')
    listCaract = Aparthment.find('ul',attrs={'property-main-features'})

    tot=tot+1
    try:
        price=Aparthment.find('p',attrs={'titlebar__price'}).get_text()
        try:
            expenses=Aparthment.find('p',attrs={'titlebar__expenses hide-in-mobile'}).get_text()
        except:
            expenses='    + $32.000 expensas   '
        direcction=Aparthment.find('h3',attrs={'titlebar__address'}).get_text()
        try:
            coveredArea =listCaract.find('li',attrs={'title':'Sup. cubierta'}).find('p',attrs={'strong'}).get_text()
        except:
            coveredArea='0 m² Cubierta'
        bedrooms =listCaract.find('li',attrs={'title':'Dormitorios'}).find('p',attrs={'strong'}).get_text()
        try:
            antiquity =listCaract.find('li',attrs={'title':'Antigüedad'}).find('p',attrs={'strong'}).get_text()
        except:
            antiquity = '10000 años'
        toilets =listCaract.find('li',attrs={'title':'Baños'}).find('p',attrs={'strong'}).get_text()
        environments =listCaract.find('li',attrs={'title':'Ambientes'}).find('p',attrs={'strong'}).get_text()
        try:
            garages =listCaract.find('li',attrs={'title':'Cocheras'}).find('p',attrs={'strong'}).get_text()
        except:
            garages = '0 cochera'
        try:
            condition =listCaract.find('li',attrs={'title':'Estado'}).find('p',attrs={'strong'}).get_text()
        except:
            condition=' '
        try:
            provision =listCaract.find('li',attrs={'title':'Disposición'}).find('p',attrs={'strong'}).get_text()
        except:
            provision=''

        listaAparthment.append( cleanData(price,expenses,direcction,coveredArea,bedrooms,antiquity,toilets,environments,garages,condition,provision) )
    except:
        print('error post')
        error=error+1
print('los casos exitos fueron: {}'.format( (tot-error) ) )
print('los casos fallidos fueron: {}' .format((error) )  )


# In[ ]:


print('el porcentaje de casos exitosos fue de: {}' .format(((tot-error)/tot )  ))


# In[ ]:


csv_headers=['currencyPurchase','pricePurchase','expensesCurrency','expensesPrice','direcction','coveredArea','bedrooms','antiquity','toilets','environments','garages','condition','provision']


# In[ ]:


def _save_cars(data_car,name,csv_headers):
    import csv
    out_file_name = '{x}.csv'.format(x=name)
    
    with open(out_file_name, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for data in data_car:
            row =data
            writer.writerow(row)


# In[ ]:


_save_cars(listaAparthment,name_csv,csv_headers)


# In[ ]:





# In[ ]:




