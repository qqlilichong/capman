
#######################################################################################################

from lxml import etree

#######################################################################################################

def xhtml(html):
    result = None
    try:
        result = etree.HTML(html)
    finally:
        return result

#######################################################################################################

def xselects(xp, path):
    result = None
    try:
        result = xp.xpath(path)
    finally:
        return result

def xselect(xp, path, i=0):
    result = None
    try:
        result = xselects(xp, path)[i]
    finally:
        return result

#######################################################################################################

def xattr(xp, attr):
    result = None
    try:
        result = xp.xpath(r'.//@%s' % attr)[0]
    finally:
        return result

def xtext(xp):
    result = None
    try:
        result = xp.xpath(r'.//text()')[0]
    finally:
        return result

#######################################################################################################
