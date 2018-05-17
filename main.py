
######################################################

from javtools import *

######################################################

if __name__ == '__main__':
    exit()
    res_path = os.path.join(os.path.dirname(__file__), 'res')

    javdict = {
        'SONE': ('SNIS',),
    }

    for maker_name, maker_plist in javdict.items():
        for pheader in maker_plist:
            maker_path = os.path.join(res_path, maker_name)
            cache_path = os.path.join(maker_path, pheader)
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)

            cache_file = os.path.join(cache_path, pheader + '.jlsc')
            jsearch = JavLibSearch(cache_file)
            if not jsearch.result:
                jsearch.getkeyword(pheader + '-')

            print(jsearch)
            jsearch.build(cache_path)

    print('capman bye!')
    exit(0)

######################################################
