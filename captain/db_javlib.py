
######################################################

import pymysql

######################################################

class JavLibDB:

    ######################################################

    def __init__(self):
        self.session = None

    ######################################################

    def ready(self):
        if self.session:
            return True

        return None

    ######################################################

    def close(self):
        try:
            if self.session:
                self.session.close()

        finally:
            self.session = None

    ######################################################

    def connect(self):
        result = None

        try:
            self.close()
            self.session = pymysql.connect(
                host='localhost',
                user='root',
                passwd='admin',
                db='javlib',
                charset='utf8mb4'
            )
            self.session.autocommit(False)

            result = True
            return

        finally:
            if not result:
                self.close()

            return result

    ######################################################

    def update(self, dbmodel):
        if not self.ready():
            return None

        result = None
        context = None

        try:
            context = self.session.cursor()

            jid = dbmodel['id']
            context.execute(self.sql_update_detail(jid, dbmodel['detail']))

            for tkey in ['maker', 'label', 'cast']:
                for model in dbmodel[tkey]:
                    context.execute(self.sql_update_url(tkey, model))
                    self.syncroute(context, jid, tkey, model[0])

            result = True
            return

        finally:
            if result:
                self.session.commit()
            else:
                self.session.rollback()

            if context:
                context.close()

            return result

    ######################################################

    @staticmethod
    def syncroute(context, jid, tkey, fkey):
        sql = 'SELECT id FROM detailroute WHERE id="%s" AND tkey="%s" AND fkey="%s" limit 1 ;' % (jid, tkey, fkey)
        result = context.execute(sql)
        if result == 0:
            context.execute('INSERT INTO detailroute VALUES (0, "%s", "%s", "%s")' % (jid, tkey, fkey))

    ######################################################

    def delete(self, dbmodel):
        if not self.ready():
            return None

        result = None
        context = None

        try:
            context = self.session.cursor()

            jid = dbmodel['id']
            context.execute('DELETE FROM detail WHERE id="%s" ;' % jid)
            context.execute('DELETE FROM detailroute WHERE id="%s" ;' % jid)

            result = True
            return

        finally:
            if result:
                self.session.commit()
            else:
                self.session.rollback()

            if context:
                context.close()

            return result

    ######################################################

    @staticmethod
    def sql_update_detail(jid, model):
        return (
            'INSERT INTO detail '
            'VALUES ("%s", "%s", "%s", "%s", "%s") '
            'ON DUPLICATE KEY UPDATE '
            'title="%s", '
            'image="%s", '
            'date="%s", '
            'length="%s" ;'
        ) % (
            jid,
            model['title'],
            model['image'],
            model['date'],
            model['length'],
            model['title'],
            model['image'],
            model['date'],
            model['length']
        )

    @staticmethod
    def sql_update_url(table, model):
        return (
            'INSERT INTO %s '
            'VALUES ("%s", "%s", "%s") '
            'ON DUPLICATE KEY UPDATE '
            'url="%s", '
            'name="%s" ;'
        ) % (
            table,
            model[0],
            model[1],
            model[2],
            model[1],
            model[2]
        )

    ######################################################

######################################################
