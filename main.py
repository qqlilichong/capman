
######################################################
# Import Section.
from javtools import *

######################################################

if __name__ == '__main__':
    maker_path = os.path.join(os.path.dirname(__file__), 'res')
    maker_path = os.path.join(maker_path, 'SONE')
    for i in ['SNIS']:
        cache_path = os.path.join(maker_path, i)
        cache_file = os.path.join(cache_path, i + '.jlsc')

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        jsearch = JavLibSearch(cache_file)
        if not jsearch.result:
            jsearch.get(i + '-')

        print(jsearch)
        jsearch.build(cache_path)

    print('capman bye!')
    exit(0)

######################################################
