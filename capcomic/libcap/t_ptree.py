
#######################################################################################################

import re
import json
import configparser

#######################################################################################################

def tojson(**kwargs):
    result = None
    try:
        result = json.dumps(kwargs, ensure_ascii=False, indent=True)
    finally:
        return result

#######################################################################################################

def fromjson(text, enc=None):
    result = None
    try:
        result = json.loads(text, encoding=enc)
    finally:
        return result

#######################################################################################################

class MyConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

#######################################################################################################

class PTini:
    def __init__(self, enc=r'utf-8'):
        self.__data = dict()
        self.__enc = enc

    def __getitem__(self, item):
        result = None
        try:
            result = self.__data[item]
        finally:
            return result

    def __update(self, cfg):
        result = None
        try:
            self.__data = {section: None for section in cfg.sections()}
            for key in self.__data.keys():
                self.__data[key] = {k: v for k, v in cfg.items(key)}
            result = self.__data
        finally:
            return result

    def read(self, filename):
        result = None
        try:
            cfg = MyConfigParser()
            cfg.read(filename, encoding=self.__enc)
            result = self.__update(cfg)
        finally:
            return result

    def smatch(self, ma, i=1):
        result = None
        try:
            ma = re.compile(ma)
            data = dict()
            for key in self.__data.keys():
                m = ma.match(key)
                if not m:
                    continue
                if not i:
                    data[key] = m
                else:
                    data[key] = m.group(i)
            result = data
        finally:
            return result

#######################################################################################################
