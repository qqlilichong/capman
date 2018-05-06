
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html, 'html5lib')
result = bsObj.findAll('span', {'class': 'green'})
for item in result:
    print(item)
