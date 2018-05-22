
######################################################

import re
from .webtools import *

######################################################

class JavLibFilter:

    ######################################################

    def __init__(self, filterlist):
        self.filterflow = None
        self.filtermap = mkdict(
            EXNAME=self.filter_exname,
            SONE_TITLE=self.filter_sone_title,
        )

        self.makeflow(filterlist)

    ######################################################

    def makeflow(self, filterlist):
        result = None

        try:
            filterflow = []
            for fname in filterlist:
                filterflow.append(self.filtermap[fname])

            self.filterflow = filterflow

            result = True
            return

        finally:
            if not result:
                self.filterflow = None

            return result

    ######################################################

    def flowing(self, **jpage):
        result = None

        try:
            for flow in self.filterflow:
                jpage = flow(jpage)
                if not jpage:
                    return

            result = jpage
            return

        finally:
            return result

    ######################################################

    @staticmethod
    def filter_exname(jpage):
        if not re.match('^\d+$', jpage['jnumer']):
            return None

        return jpage

    ######################################################

    @staticmethod
    def filter_sone_title(jpage):
        if re.match('.*（ブルーレイディスク）', jpage['title']):
            return None

        return jpage

    ######################################################

######################################################
