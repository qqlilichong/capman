
#######################################################################

from javlib import JavLibSearch, JavLibStore

#######################################################################

def main():
    typedict, videodict = JavLibSearch.search(r'http://www.k25m.com/ja/vl_searchbyid.php?keyword=AVOP')
    JavLibStore.store(r'Y:/JavLibrary', r'AVOPEN',
                      {r'db': r'javlib', r'user': r'root', r'passwd': r'admin'},
                      typedict, videodict)
    print('bye...')

#######################################################################


if __name__ == "__main__":
    main()


#######################################################################
