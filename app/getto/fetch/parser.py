import requests
from bs4 import BeautifulSoup
import lxml
import re
from typing import Dict

class Parser:
    def __init__(self, url: str, selector: Dict) ->None:
        '''
        first import name and link to scape data
        '''
        self.url = url
        self.page = self.get_page()
        self.selector = selector
    def get_page(self):
        '''
        take an url as argument and return an BeautifulSoup Object
        also, set the self page = this object
        '''
        try: 
            source = requests.get(self.url).text
        except  requests.exceptions.RequestException:
            return None
        return BeautifulSoup(source, 'lxml')
    def select_element(self, selector):
        '''
        take an Beautiful Object and param, set the self elements and return a string
        '''
        elements = self.page.select(selector)
        if elements is not None and len(elements) > 0:
            return '\n'.join([elem.get_text() for elem in elements])
        return ''    
    def get_data(self):
        return {key:self.select_element(value) for (key,value) in self.selector.items()}
    
def get_url(link, comparing):
    chapter_list_source = requests.get(link).text
    r = BeautifulSoup(chapter_list_source, 'lxml')
    chapter_list = r.select(comparing)
    # urls = [e.a.attrs['href'] for e in chapter_list]
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(chapter_list))
