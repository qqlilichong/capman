
#######################################################################

from dbe import DBEngine
from javlib import JavLibDetail, JavLibSearch

#######################################################################

def main():
    dbs = DBEngine()
    dbs.connect(db='javlib', user='root', passwd='admin')
    #javdetail = JavLibDetail(r'http://www.k25m.com/ja/?v=javlijyuze', r'S1')
    #javdetail.savemodel(dbs)
    javsearch = JavLibSearch(r'http://www.k25m.com/ja/vl_searchbyid.php?keyword=AVOP-')
    print('bye...')

#######################################################################


if __name__ == "__main__":
    main()


#######################################################################
