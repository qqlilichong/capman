
#######################################################################

from dbe import DBEngine
from javlib import JavLibDetail

#######################################################################

def main():
    dbs = DBEngine()
    dbs.connect(db='javlib', user='root', passwd='admin')
    javdetail = JavLibDetail(r'http://www.k25m.com/ja/?v=javlijyuze', r'S1')
    javdetail.savemodel(dbs)
    print('bye...')

#######################################################################


if __name__ == "__main__":
    main()


#######################################################################
