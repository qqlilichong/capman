
######################################################

from javtools import *

######################################################

if __name__ == '__main__':
    res_path = os.path.join(os.path.dirname(__file__), 'res')

    javdict = {
        'SONE': ('SNIS',),
    }

    for maker_name, maker_plist in javdict.items():
        for pheader in maker_plist:
            image_path = os.path.join(res_path, maker_name)
            image_path = os.path.join(image_path, pheader)

            jsearch = JavLibSearch(os.path.join(res_path, pheader + '.jlsc'))
            if not jsearch.ready():
                jsearch.getkeyword(pheader + '-')

            if jsearch.ready():
                jsearch.build(image_path)

            print(jsearch)

    print('capman bye!')
    exit(0)

######################################################
