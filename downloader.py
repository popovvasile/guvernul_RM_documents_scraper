# -*- coding: utf-8 -*-
from __future__ import ( division, absolute_import, print_function, unicode_literals )
import sys, os, tempfile, logging
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bsoup
import requests,urllib2,urlparse
import requests as rq
import re
import json, ast  
import unicodedata



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

def date():
    date = search_sites()

    date = [w.replace('/ro/content/sedinta-guvernului-din-', '') for w in date]
    date = [w.replace('-', ' ') for w in dates] 
    return date

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


def download_file(url, desc=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb+') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename
def list_of_links():
    elements = search_sites()
    list_links=[]
    for i in elements:
        elements2 = search_files(i)
        for e in elements2:
            list_links.append(e)
    return list_links



#def this_shity_scraper(BASE_URL):
 

def downloader():
    list_of_download_links = list_of_links()
    for i in list_of_download_links:
        download_file(i)
downloader()