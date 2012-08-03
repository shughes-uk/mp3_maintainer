#!/usr/bin/env python

import os
import os.path
import sys


def escape_quotes(path):
    return path.replace('"', r'\"')



def encode_mp3(flac_file):
    mp3_file, ext = os.path.splitext(flac_file)
    mp3_file = escape_quotes(mp3_file + '.mp3')
    command = 'ffmpeg -i %s -map_metadata 0:s:0 -id3v2_version 4 -ab 192k -ac 2 -ar 48000 %s' %(flac_file,mp3_file)
    os.system(command)


def main(argv):
    source = argv[1]
    target = argv[2]    
    if os.path.isdir(source) and os.path.isdir(target):
            for x in source:

                

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: %s <source dir> <target dir>' % (sys.argv[0])
        sys.exit(1)

    main(sys.argv[1:])