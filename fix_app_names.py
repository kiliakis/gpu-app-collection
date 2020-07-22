#!/usr/bin/env python

import argparse
import re
import os
import shutil
import stat

name_replacements = {
    '{}-ispass2009-1.0': 'ispass-2009-(.*)',
    '{}-parboil-0.2': 'parboil-(.*)'
}


def copy(source, target):
    if source == target:
        return
    # copy content, stat-info, etc
    shutil.copy2(source, target)
    # copy owener and group
    st = os.stat(source)
    os.chown(target, st[stat.ST_UID], st[stat.ST_GID])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Analyze the output file to re-construct an active warps trace.')

    parser.add_argument('-i', '--indir', type=str, default=None,
                        help='The directory with the executables.')

    parser.add_argument('-o', '--outdir', type=str, default=None,
                        help='The directory to store the resulting executables.'
                        'Default: the same as the indirectory.')

    args = parser.parse_args()

    if not args.outdir:
        args.outdir = args.indir
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    for k, v in name_replacements.items():
        name_replacements[k] = re.compile(v)

    for infile in os.listdir(args.indir):
        if os.path.isfile(os.path.join(args.indir, infile)):
            outfile = infile
            for k, v in name_replacements.items():
                match = v.search(infile)
                if match:
                    name = match.groups()[0]
                    outfile = k.format(name)
                    break
            copy(os.path.join(args.indir, infile),
                 os.path.join(args.outdir, outfile))
