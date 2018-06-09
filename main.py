
######################################################

from captain.sp_javlib_search import *

######################################################

if __name__ == '__main__':
    jpath = os.path.join(os.path.dirname(__file__), 'javlib')
    jsite = 'http://www.javlibrary.com/ja/'
    jfilter = ['EXNAME', 'SONE_TITLE', 'AVOP_PASS']

    jurl, jmaker = ('vl_maker.php?m=aria', 'PREMIUM')
    scrapy_javlib_maker(jpath, jsite + jurl, jmaker.upper(), jfilter)

    print('capman bye!')
    exit()

######################################################
