
from javtools import *

url = 'http://www.javlibrary.com/ja/?v=javlilaf5y'
pagedict = javlib_parse_html('./res/snis.html', url)
print(javlib_check_lost(pagedict))
