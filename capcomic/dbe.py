
#######################################################################

import pymysql

#######################################################################

class DBEngine:
    def __init__(self):
        self.session = None
        self.sqls = None

    def connect(self, **kwargs):
        result = None
        try:
            if self.session:
                return

            if r'host' not in kwargs.keys():
                kwargs[r'host'] = r'localhost'

            if r'charset' not in kwargs.keys():
                kwargs[r'charset'] = r'utf8mb4'

            self.session = pymysql.connect(**kwargs, autocommit=False)
            if not self.session:
                return

            self.sqls = list()
            result = self.session
        finally:
            return result

    def ready(self):
        return self.session

    def cursor(self):
        result = None
        try:
            if not self.ready():
                return

            result = self.session.cursor()
        finally:
            return result

    def append(self, sql):
        result = None
        try:
            if not self.ready():
                return

            self.sqls.append(sql)
            result = True
        finally:
            return result

    def commit(self):
        cursor = self.cursor()
        if not cursor:
            return None

        result = None
        try:
            for params in self.sqls:
                templ = params.pop(0)
                cursor.execute(templ, [pymysql.escape_string(param) for param in params])
        except:
            self.session.rollback()
        else:
            self.session.commit()
            result = True
        finally:
            cursor.close()
            self.sqls.clear()
            return result

    def replace(self, tname, **kwargs):
        result = None
        try:
            keys = list()
            vals = list()
            emps = list()
            for k, v in kwargs.items():
                keys.append(k)
                vals.append(v)
                emps.append(r'%s')

            vals.insert(0, r'REPLACE INTO %s (%s) VALUES (%s) ;' % (tname, r','.join(keys), r','.join(emps)))
            result = self.append(vals)
        finally:
            return result

#######################################################################
