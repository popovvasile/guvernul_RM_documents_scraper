# coding: utf-8
import json
import requests
from bs4 import BeautifulSoup
import re


def spider_web(max_pages):
    page = 0
    links = []
    true_links = []
    file1 = []
    while page <= max_pages:
        url = "http://lex.justice.md/index.php?search=true&current_page=%s"
        url = url % page
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', href=True):
            href = "http://lex.justice.md" + link.get('href')
            links.append(href)
        page += 1
    #print(links)

    for items in links:
        if items.startswith("http://lex.justice.md/index.php?action=view&view=doc&lang=1&id="):
            true_links.append(items)
    #print(true_links)

    for urls in true_links:
        source_code = requests.get(urls)
        source_text = source_code.text
        soup = BeautifulSoup(source_text)
        soup1 = soup.find('table', {'id': 'master'})
        number1 = BeautifulSoup(str(soup1))
        allnr = number1.findAll('tr')
        text = BeautifulSoup(str(allnr))
        all_text = text.get_text(separator=' ', strip=True)
        pattern = re.compile('Nr\. \d+')
        numbers = re.findall(pattern, all_text)
        numbers1 = numbers[0]
        #print(numere1)
        all_header = number1.findAll('span', {'class': 'doc_header'})
        all_header1 = BeautifulSoup(str(all_header))
        all_header2 = all_header1.get_text(separator=' ', strip=True)
        print(all_header2.encode())
        for allla in text.findAll('td', {'class': 'noborder'})[7:]:
            all_text = allla.get_text(separator=' ', strip=True)
            s = all_text.replace('\\xa0', "")
            #s.encode()
            #print(s.encode())
            file = [{'number': numbers1, "title": all_header2, "body": s}]
            file1.append(file)
            #print (file)
    return json.dumps(file1)

with open('eo.json', 'w') as eo:
    eo.write(spider_web(1))
