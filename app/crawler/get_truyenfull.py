from bs4 import BeautifulSoup
import lxml
import requests

for i in range(2425):
    link = "https://truyenfull.vn/pham-nhan-tu-tien/chuong-"+ str(1+i)
    file = requests.get(link).text
    bs = BeautifulSoup(file, "lxml")
    elements = bs.select_one(".chapter-c")
    title = bs.title.get_text()
    elements = str(elements).replace("div", "p")
    elements = elements.replace("<br/><br/>", "</p><p>")
    f = open(f'{i}_{title}.txt', "w", encoding="utf-8")
    f.write(elements)
    f.close()
    print(f"{title} is written to the file")
