
#######################################################################

import os
import webtool
import caper_dmwu

#######################################################################

def capman():
    cfg = webtool.IniDict()
    cfg.read(os.path.join(os.path.dirname(__file__), r'caper.ini'))
    for maker in cfg.resection(r'^DMWU_(\w+)$').keys():
        caper_dmwu.capman(cfg[maker][r'url'],
                          os.path.join(cfg[r'OUTPUT'][r'path'], cfg[maker][r'title']),
                          cfg[maker][r'match'],
                          cfg[maker][r'format'],
                          cfg[maker][r'formatfill'],
                          cfg[maker][r'reverse'])

#######################################################################

if __name__ == "__main__":
    capman()
    print('bye...')

#######################################################################
