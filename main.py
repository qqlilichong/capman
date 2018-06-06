
######################################################

from captain.sp_javlib_search import *

######################################################

if __name__ == '__main__':
    path_root = os.path.join(os.path.dirname(__file__), 'javlib')
    jsite = 'http://www.javlibrary.com/ja/'

    jurl = jsite + 'vl_maker.php?m=aq4q'
    jmaker = 'IDEAPOCKET'

    jfilter = ['EXNAME', 'SONE_TITLE', 'AVOP_PASS']
    scrapy_javlib_maker(path_root, jurl, jmaker.upper(), jfilter)

    print('capman bye!')
    exit()

######################################################
