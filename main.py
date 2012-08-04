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

def cleanRecursive(directory):
    for root , subfolders , files in os.walk(directory ,topdown=False):
        for x in files:
            name , extension = os.path.splitext(x)
            if extension.lower() != '.flac':
                outfileName = os.path.join(root, x)
                os.remove(outfileName)
        for subfolder in subfolders:
            path = os.path.join(root,subfolder)
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
def main(opts , argv):
    source = argv[1]
    target = argv[2]    
    if os.path.isdir(source):
        if opts.remove:
            cleanRecursive(source)
        for root , subfolders , files in os.walk(source):
            



if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-r', '--remove', help='removes non flac files and empty folders from source', dest='remove', default=False, action='store_true')
    (opts, args) = parser.parse_args()
    if len(args) != 2:
        print 'usage: %s <source dir> <target dir>' % (sys.argv[0])
        sys.exit(1)

    main(opts , sys.argv[1:])