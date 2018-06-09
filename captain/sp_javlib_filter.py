
######################################################

import re

######################################################

class JavLibFilter:

    ######################################################

    def __init__(self, jfilterflow):
        self.filterflow = None
        self.actions = {
            'match': self.action_match
        }
        self.makeflow(jfilterflow)

    ######################################################

    def makeflow(self, jfilterflow):
        result = None

        try:
            filterflow = []
            for key, val in jfilterflow:
                act = key.split('.')
                if act[0] in self.actions:
                    act.append(re.compile(val))
                    filterflow.append(act)
                    continue
                return

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
            for act in self.filterflow:
                jpage = self.actions[act[0]](act, jpage)
                if not jpage:
                    return

            result = jpage
            return

        finally:
            return result

    ######################################################

    @staticmethod
    def action_match(act, jpage):
        if act[-1].match(jpage[act[1]]):
            return None
        return jpage

    ######################################################

######################################################
