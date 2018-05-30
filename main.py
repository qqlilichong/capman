
######################################################

from captain.sp_javlib_search import *

######################################################

if __name__ == '__main__':
    path_root = os.path.join(os.path.dirname(__file__), 'javlib')

    jurl = 'http://www.javlibrary.com/ja/vl_maker.php?m=aqra'
    jmaker = 'MOODYZ'
    jfilter = ['EXNAME', 'SONE_TITLE', 'AVOP_PASS']
    scrapy_javlib_maker(path_root, jurl, jmaker, jfilter)

    print('capman bye!')
    exit()

######################################################
