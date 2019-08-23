
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

def xnode(xp, node):
    result = None
    try:
        result = xp.xpath(r'.//%s' % node)[0]
    finally:
        return result

def xattr(xp, attr):
    return xnode(xp, r'@%s' % attr)

def xtext(xp):
    return xnode(xp, r'text()')

#######################################################################################################
