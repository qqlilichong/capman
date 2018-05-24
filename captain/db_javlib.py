
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

    def update(self, jdetail):
        result = None
        context = None

        try:
            if not self.ready():
                return

            context = self.session.cursor()
            context.execute(self.sql_delete_detail(jdetail))
            self.session.commit()

            result = True
            return

        finally:
            if context:
                context.close()

            return result

    ######################################################

    def delete(self, jdetail):
        result = None
        context = None

        try:
            if not self.ready():
                return

            context = self.session.cursor()
            context.execute(self.sql_delete_detail(jdetail))
            self.session.commit()

            result = True
            return

        finally:
            if context:
                context.close()

            return result

    ######################################################

    @staticmethod
    def sql_update_detail(jdetail):
        return (
            'INSERT INTO detail (id, title, image, date, length, maker, label, cast) '
            'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") '
            'ON DUPLICATE KEY UPDATE '
            'title="%s", '
            'image="%s", '
            'date="%s", '
            'length="%s", '
            'maker="%s", '
            'label="%s", '
            'cast="%s" ;'
        ) % (
            jdetail['id'],
            jdetail['title'],
            jdetail['image'],
            jdetail['date'],
            jdetail['length'],
            jdetail['maker'],
            jdetail['label'],
            jdetail['cast'],
            jdetail['title'],
            jdetail['image'],
            jdetail['date'],
            jdetail['length'],
            jdetail['maker'],
            jdetail['label'],
            jdetail['cast']
        )

    @staticmethod
    def sql_delete_detail(jdetail):
        return 'DELETE FROM detail WHERE id = "%s" ;' % jdetail['id']

    ######################################################

######################################################
