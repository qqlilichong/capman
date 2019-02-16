
#######################################################################

import os
import sys
import t_webtool

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 4:
        print(r'.py data.txt dir_src dir_dst fixext[opt]')
        sys.exit(0)

    datafile = sys.argv[1]
    dir_src = sys.argv[2]
    dir_dst = sys.argv[3]

    fixext = None
    if argc >= 5:
        fixext = sys.argv[4]

    data = [line.strip() for line in t_webtool.fget(datafile).decode(r'utf-8').split('\n') if line]

    result = 0
    t_webtool.fmkdir(dir_dst)
    for file_src in [os.path.join(dir_src, f) for f in data]:
        if not os.path.exists(file_src):
            continue

        file_dst = os.path.join(dir_dst, os.path.basename(file_src))
        if fixext:
            fl = file_dst.split(r'.')
            fl.insert(-1, fixext)
            file_dst = r'.'.join(fl)

        t_webtool.fset(file_dst, t_webtool.fget(file_src))
        result += 1

    print(r'result : %s' % result)

#######################################################################
