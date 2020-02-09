
#######################################################################################################

from libcap import a_tool

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def __fixtitle(text):
    return text.replace('\\', r'').replace('/', r'')

def uc(param):
    bact = param[r'bact']
    farmer = param[r'farmer']
    for k, v in bact.view.items():
        for pin in farmer.pin.values():
            pin[v] = __fixtitle(pin[k])
    return param

#######################################################################################################
