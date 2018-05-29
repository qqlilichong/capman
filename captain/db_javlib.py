
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

        def core(jd, ctx):
            ctx.execute(self.sql_update_detail(jd))

            for maker in jd.maker:
                ctx.execute(self.sql_update_url('maker', maker))

            for label in jd.label:
                ctx.execute(self.sql_update_url('label', label))

            for cast in jd.cast:
                ctx.execute(self.sql_update_url('cast', cast))

            return True

        return self.execute(jdetail, core)

    ######################################################

    def execute(self, jdetail, handler):
        result = None
        context = None

        try:
            if not self.ready():
                return

            if not jdetail.ready():
                return

            context = self.session.cursor()
            if not handler(jdetail, context):
                return

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
    def sql_update_detail(jdetail):
        jid = jdetail.id
        jurl = jdetail.url
        jtitle = jdetail.title
        jimage = jdetail.image
        jdate = jdetail.date
        jlength = jdetail.length
        jmaker = ';'.join([x[0] for x in jdetail.maker])
        jlabel = ';'.join([x[0] for x in jdetail.label])
        jcast = ';'.join([x[0] for x in jdetail.cast])

        return (
            'INSERT INTO detail '
            'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") '
            'ON DUPLICATE KEY UPDATE '
            'url="%s", '
            'title="%s", '
            'image="%s", '
            'date="%s", '
            'length="%s", '
            'maker="%s", '
            'label="%s", '
            'cast="%s" ;'
        ) % (
            jid,
            jurl,
            jtitle,
            jimage,
            jdate,
            jlength,
            jmaker,
            jlabel,
            jcast,
            jurl,
            jtitle,
            jimage,
            jdate,
            jlength,
            jmaker,
            jlabel,
            jcast,
        )

    @staticmethod
    def sql_update_url(tname, fkey):
        return (
            'INSERT INTO %s '
            'VALUES ("%s", "%s", "%s") '
            'ON DUPLICATE KEY UPDATE '
            'url="%s", '
            'name="%s" ;'
        ) % (
            tname,
            fkey[0],
            fkey[2],
            fkey[1],
            fkey[2],
            fkey[1]
        )

    ######################################################

######################################################
