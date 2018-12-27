
#######################################################################

import pymysql

#######################################################################

class DBEngine:
    def __init__(self):
        self.session = None

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

    def commit(self, sqls):
        cursor = self.cursor()
        if not cursor:
            return None

        result = None
        try:
            for it in sqls:
                data = list()
                data += it
                templ = data.pop(0)
                args = list()
                for arg in data:
                    args.append(pymysql.escape_string(arg))
                cursor.execute(templ, args)
        except:
            self.session.rollback()
        else:
            self.session.commit()
            result = True
        finally:
            cursor.close()
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

            vals.insert(0, r'REPLACE INTO %s (%s) VALUES (%s) ;' % (tname, ','.join(keys), ','.join(emps)))
            result = self.commit([vals])
        finally:
            return result

#######################################################################
