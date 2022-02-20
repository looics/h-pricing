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
houseprice = []
propname = []
proploc = []
propinfo = []
propinfo1 = []
propinfo2 = []
propinfo3 = []
#numpage = 68486/24
numpage = 70281/24
print(numpage)
for i in range(500):
    url = 'https://www.iproperty.com.my/sale/kuala-lumpur/all-residential/?l1&page=' + str(i)
    print('Scraping URL:', url)
    randomtime = random.randrange(20, 60)
    
    iprophtmlfile = 'iprophtml_{}.csv'.format(i)
    iprophousefile = 'iprophouselist_{}.csv'.format(i)
    
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    from selenium import webdriver
    from webdriver_manager.firefox import GeckoDriverManager
    
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    browser.get(url)
    html = browser.execute_script("return document.documentElement.outerHTML")
    htmlhouselist = []
    br_soup = BeautifulSoup(html, 'html.parser')
    #col_list = br_soup.find('div', 'listing-widget-new small-listing-card')
    #print(col_list)
    house_list = br_soup.find_all('div', 'PremiumCardstyle__CardWrapper-cvkMVX jRRXhG')
    #print(house_list)
    htmlhouselist.append(house_list)
    df_htmllink = pd.DataFrame({'link': htmlhouselist})
    df_htmllink.to_csv(iprophtmlfile, sep='\t', encoding='utf-8')
    #price = br_soup.find_all('h5', class_='listing-price')
    #print(price.text)

    
    for lists in house_list:
        price = lists.find('div', class_='ListingPricestyle__ListingPriceWrapper-eZrVug gUGYlt listing-price').text
        houseprice.append(price)
        print(price)
        #psqf = lists.find('div', class_='ListingPricestyle__PricePSFWrapper-iaipCH ccOfpl listing-price-psf').text
        '''name = lists.find('div', class_='detail-property').text
        print(name)'''
        name2 = lists.find('h2', class_='PremiumCardstyle__TitleWrapper-cBmVrL ePWFgo')
        name2 = re.sub('(<.*?>)', '', str(name2))
        propname.append(name2)
        print(name2)
        location = lists.find('div', class_='PremiumCardstyle__AddressWrapper-ldsjqp gRJjrp').text
        proploc.append(location)
        print(location)
        #property_type = lists.find('ul', class_='listing-property-type').text
        #print(property_type)'''
        property_info = lists.find('p', class_='ListingAttributesstyle__ListingAttrsDescriptionItemWrapper-fQKuaA fJmpgN attributes-description-item').text
        propinfo.append(property_info)
        print(property_info)
        property_bedroom = lists.find('li', class_='ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper bedroom-facility')
        property_bedroom = re.sub('(<.*?>)', '', str(property_bedroom))
        propinfo1.append(property_bedroom)
        print(property_bedroom)
        property_bathroom = lists.find('li', class_='ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper bathroom-facility')
        property_bathroom = re.sub('(<.*?>)', '', str(property_bathroom))
        propinfo2.append(property_bathroom)
        print(property_bathroom)
        property_carporch = lists.find('li', class_='ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF eAeBYm attributes-facilities-item-wrapper carPark-facility')
        property_carporch = re.sub('(<.*?>)', '', str(property_carporch))
        propinfo3.append(property_carporch)
        print(property_carporch)
        
    
    df_house = pd.DataFrame({'Property Name': propname, 'Property Location': proploc,
                                    'Price': houseprice, 'Property Info': propinfo, 
                                    'Bedroom': propinfo1, 
                                    'Bathroom': propinfo2, 'Car Porch': propinfo3})
    
    df_house.to_csv(iprophousefile, sep='\t', encoding='utf-8')
    print(randomtime, "seconds")
    time.sleep(randomtime)
    browser.close()

