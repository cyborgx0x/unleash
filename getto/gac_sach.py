
from .fetch import Parser
from urllib.parse import urlparse
from typing import Dict

class GacSach(Parser):
    book_tag = {
        "title": ".page-title",
        "cover": ".imagesach",
        "author": ".field-name-field-author",
        "category": ".field-name-field-mucsach",
    }
    def  __init__(self, url: str, selector: Dict=None) -> None:
        self.selector = self.book_tag
        super().__init__(url, selector)
    def get_sub_link(self):
        elements = self.page.select(".book-nav")
        if elements is not None and len(elements) > 0:
            for i in elements:
                r = i.select(".menu")
                for k in r: 
                    return [urlparse(self.url)._replace(path = n.get('href')).geturl() for n in k.find_all("a")]
    def get_chapter_content(self):
        chapter_tag= {
            "title": ".page-title",
            "content": ".field-name-body"
        }
        return ([Parser(i, chapter_tag).get_data() for i in self.get_sub_link()])
