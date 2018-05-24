
######################################################

from captain.sp_javlib_search import *
from captain.db_javlib import *

######################################################

if __name__ == '__main__':
    id_maker = 'SONE'
    id_typer = 'SSNI'
    jfilter = ['EXNAME', 'SONE_TITLE']
    path_cache = os.path.join(os.path.dirname(__file__), 'res')
    path_maker = os.path.join(path_cache, id_maker)
    cache_file = os.path.join(path_cache, '%s.jlsc' % id_typer)

    jsearch = JavLibSearch(cache_file)

    if not jsearch.ready():
        jsearch.get('http://www.javlibrary.com/ja/vl_searchbyid.php?&keyword=%s' % id_typer, jfilter)

    if jsearch.ready():
        print(jsearch)
        jsearch.build(path_maker)

    print('capman bye!')
    exit(0)

######################################################
