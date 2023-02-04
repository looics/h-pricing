# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 12:39:21 2021

@author: looi
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import math
import time
import random
import os

os.environ['GH_TOKEN'] = "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"

houseprice = []
propname = []
proploc = []
propinfo = []
propinfo1 = []
propinfo2 = []
propinfo3 = []

#url = 'https://www.iproperty.com.my/sale/kuala-lumpur/all-residential/?l1&page=' + str(i)

for i in range(1, 7968):
    url = 'https://www.edgeprop.my/buy/kuala-lumpur/all-residential?page=' + str(i)
    print('Scraping URL:', url)
    randomtime = random.randrange(20, 50)
    
    prophtmlfile = 'edgeprop2/prophtml_{}.csv'.format(i)
    prophousefile = 'edgeprop2/prophouselist_{}.csv'.format(i)
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    
    from selenium import webdriver
    from webdriver_manager.firefox import GeckoDriverManager
       
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    browser.get(url)
    html = browser.execute_script("return document.documentElement.outerHTML")
    htmlhouselist = []
    br_soup = BeautifulSoup(html, 'html.parser')
    house_list = br_soup.find_all('div', 'd-flex align-items-start flex-column h-100')
    
    for lists in house_list:
        price = lists.find('h5', class_='listing-price').text
        houseprice.append(price)
        print(price)
        
        name = lists.find('h3', class_='listing-name').text
        propname.append(name)
        print(name)
        
        location = lists.find('p', class_='listing-address').text
        proploc.append(location)
        print(location)
        
        try:
            property_info = lists.find('div', class_='listing-specs').text
            propinfo.append(property_info)
            print(property_info)
        except:
            propinfo.append('New Project')
            print('New Project')
    
    df_house = pd.DataFrame({'Property Name': propname, 'Property Location': proploc,
                             'Price': houseprice, 'Property Info': propinfo
                             })

    df_house.to_csv(prophousefile, sep='\t', encoding='utf-8')
    print(randomtime, "seconds")
    time.sleep(randomtime)

    browser.close()
    


