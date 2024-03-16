import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--id', type=str, required=True)

args = parser.parse_args()
print(args.id)

url = "https://www.sieuthivienthong.com/searchresult.html"
payload={'seracharg': args.id}
headers = {
  'Cookie': 'PHPSESSID=ec4kb77cahjtpckv4e5hvehni2'
}
response = requests.request("POST", url, headers=headers, data=payload).text

page = BeautifulSoup(response, 'lxml')
elements = page.select(".list_prod_home")

li = elements[0].select('li')
for i in li:
    # print(i.select('a')[0]['href'])
    print(i.select('.name_prod_home')[0].get_text())
    print(i.select('.nb_price_prod_home')[0].get_text())
# [urlparse(url)._replace(path = n.get('href')).geturl() for n in k.find_all("a")]


# link = "https://www.sieuthivienthong.com/camera-ip-dome-hong-ngoai-8.0-megapixel-hikvision-ds-2cd2386g2-isusl-46272.html"
# from fetch import Parser

# tag = {
#     "title": "title",
#     "price": ".price_prod_articles",
# }

# r = Parser(link, tag)
# print(r.get_data())