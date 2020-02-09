
#######################################################################################################

from libcap import a_tool

def meta():
    return a_tool.metatbl(globals())

#######################################################################################################

def uc(param):
    bact = param[r'bact']
    farmer = param[r'farmer']
    np = dict()
    for k, v in bact.view.items():
        np[v] = farmer.reparamval(k)
    farmer.pin[np[r'pin.id']] = np
    return param

#######################################################################################################
