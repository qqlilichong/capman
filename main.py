from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html, 'lxml')
result = bsObj.findAll('span', {'class': 'red'})
for item in result:
    print(item)
