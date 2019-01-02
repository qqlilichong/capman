
#######################################################################

from javlib import JavLibSearch

#######################################################################

def main():
    javsearch = JavLibSearch(r'http://www.k25m.com/ja/vl_searchbyid.php?keyword=AVOP',
                             r'AV1',
                             {r'db': r'javlib', r'user': r'root', r'passwd': r'admin'})
    print('bye...')

#######################################################################


if __name__ == "__main__":
    main()


#######################################################################
