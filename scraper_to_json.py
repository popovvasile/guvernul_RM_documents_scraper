# -*- coding: utf-8 -*-
from __future__ import ( division, absolute_import, print_function, unicode_literals )
import sys, os, tempfile, logging
from bs4 import BeautifulSoup

import requests,urllib2,urlparse
 
import unicodedata

def search_files(url1): 
    download_links =[]
    keyword = "pdf"
    r = requests.get(url1)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is None:
            continue
        elif keyword in href:  
            download_links.append(href)

    return download_links

def search_sites():
    sites =[]
    
    for i in range(0,4):
        url = "http://www.gov.md/ro/advanced-page-type/sedinte-de-guvern?date_filter[value]&page=%d" % i
        
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        keyword = "sedinta-guvernului"
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is None:
                continue
            elif keyword in href:  
                sites.append(href)
    aces = ["http://www.gov.md/" + sites for sites in sites]          
    return aces
def list_of_links():
    elements = search_sites()
    list_links=[]
    for i in elements:
        elements2 = search_files(i)
        for e in elements2:
            list_links.append(e)
    return list_links
 
def main_scraper(BASE_URL1):
    
    def get_html(url):
        response = urllib2.urlopen(url)
        return response.read()
    def ministers_names(url):
        
        ministers =[]
        keyword1 = "dl"
        keyword2 = "dna"
        html = get_html(url)

        soup = BeautifulSoup(html)

        gov_member = soup.find_all('div', class_="field-content")
        gov_mem = str(gov_member)
        gov = BeautifulSoup(gov_mem)
        test = gov.get_text()
        test1= unicodedata.normalize('NFKD', test).encode('ascii','ignore')
        list_of_min = test1.split(',')
        for i in list_of_min:
            if keyword1 in i:
                ministers.append(i)
            elif keyword2 in i:
                ministers.append(i)
        
        return ministers

    names = ministers_names(BASE_URL1)
    
    def parse(html):
        soup = BeautifulSoup(html)
        number = soup.findAll('span', class_='field-content')
      
        number = str(number)
        
        soup2 = BeautifulSoup(number)
        
        future_str= soup2.get_text()
        
        return future_str

    future_dict_str = parse(get_html(BASE_URL1))

    transfer= unicodedata.normalize('NFKD', future_dict_str).encode('ascii','ignore')
    future_dict_list = transfer.split(',')

    def filter_(list_):
        new_list=[]
        for i in list_:
            if len(i)>4:
                new_list.append(i)
        return new_list


    descriptions=(filter_(future_dict_list))

    names = ministers_names(BASE_URL1)

    list_links=search_files(BASE_URL1)
    def json_generator():  
        json =[]

        for i in range(len(names)):
            json.append({
                'name':names[i],
                'description':descriptions[i],
                'link':list_links[i]
            })
    
        return json
    final_json=json_generator()
    return final_json
    print(final_json)

BASE_URL=search_sites()
final_json_total=[]
for i in BASE_URL:
    final_json_total=main_scraper(i)
print(final_json_total)