
#######################################################################

import pymysql

#######################################################################

class DBEngine:
    def __init__(self):
        self.__session = None
        self.__sqls = None
        self.__tcols = dict()

    def connect(self, **kwargs):
        result = None
        try:
            if self.__session:
                return

            if r'host' not in kwargs.keys():
                kwargs[r'host'] = r'localhost'

            if r'charset' not in kwargs.keys():
                kwargs[r'charset'] = r'utf8mb4'

            self.__session = pymysql.connect(**kwargs, autocommit=False)
            if not self.__session:
                return

            self.__sqls = list()
            result = self.__session
        finally:
            return result

    def ready(self):
        return self.__session

    def __cursor(self):
        result = None
        try:
            if not self.ready():
                return

            result = self.__session.cursor()
        finally:
            return result

    def __cols(self, tname):
        if tname in self.__tcols:
            return self.__tcols[tname]

        cursor = self.__cursor()
        if not cursor:
            return None

        result = None
        try:
            cursor.execute(r'SELECT * FROM %s LIMIT 1' % tname)
            result = [t[0].lower() for t in cursor.description]
        finally:
            if result:
                self.__tcols[tname] = result

            cursor.close()
            return result

    def append(self, sql):
        result = None
        try:
            if not self.ready():
                return

            self.__sqls.append(sql)
            result = True
        finally:
            return result

    def commit(self):
        cursor = self.__cursor()
        if not cursor:
            return None

        result = None
        try:
            for params in self.__sqls:
                templ = pymysql.escape_string(params.pop(0))
                cursor.execute(templ, [pymysql.escape_string(param) for param in params])
        except:
            self.__session.rollback()
        else:
            self.__session.commit()
            result = True
        finally:
            cursor.close()
            self.__sqls.clear()
            return result

    def replace(self, tname, **kwargs):
        result = None
        try:
            tcols = self.__cols(tname)
            if not tcols:
                return

            keys = list()
            vals = list()
            emps = list()
            for k, v in kwargs.items():
                k = k.lower()
                if k not in tcols:
                    continue

                keys.append(k)
                vals.append(v)
                emps.append(r'%s')

            if not keys:
                return

            vals.insert(0, r'REPLACE INTO %s (%s) VALUES (%s) ;' % (tname, r','.join(keys), r','.join(emps)))
            result = self.append(vals)
        finally:
            return result

#######################################################################
