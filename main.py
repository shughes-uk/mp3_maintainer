#!/usr/bin/env python

import os
import os.path
import sys


def escape_quotes(path):
    return path.replace('"', r'\"')

def encode_mp3(flac_file,mp3_file):
    command = """ffmpeg -i "%s" -map_metadata 0:s:0 -id3v2_version 4 -ab 192k -ac 2 -ar 48000 "%s" """ %(flac_file,mp3_file)
    os.system(command)

def cleanRecursive(directory):
    for root , subfolders , files in os.walk(directory ,topdown=False):
        for x in files:
            name , extension = os.path.splitext(x)
            if extension.lower() != '.flac':
                outfileName = os.path.join(root, x)
                print 'Deleting file %s' %outfileName
                os.remove(outfileName)
        for subfolder in subfolders:
            path = os.path.join(root,subfolder)
            if len(os.listdir(path)) == 0:
                print 'Removing directory %s' %path
                os.rmdir(path)

def main(opts , argv):
    source = argv[1]
    target = argv[2]
    print 'Flac --> Mp3 maintainer running on source dir : %s , target dir : %s' %(source,target)    
    if os.path.isdir(source):
        if opts.remove:
            'Cleaning empty folders and non flac files from source directory'
            cleanRecursive(source)
        if not os.path.isdir(target):
            os.mkdir(target)

        for root , subfolders , files in os.walk(source):
            for subfolder in subfolders:
                #recreate every subfolder in this folder if it doesn't exist in target directory
                path = os.path.join(root,subfolder)
                dr = path.lstrip(source)
                dr = os.path.join(target,dr)
                if not os.path.isdir(dr):
                    os.mkdir(dr)

            for x in files:
                name , extension = os.path.splitext(x)
                if extension.lower() == '.flac':
                    #if its a flac file we want to convert to and an mp3 in the target directory
                    #if it doesn't already exist there
                    mp3_file = escape_quotes(name + '.mp3')
                    dr = root.lstrip(source)
                    dr = os.path.join(target,dr)
                    f = os.path.join(dr ,mp3_file)
                    #add option to overwrite existing mp3s
                    if not os.path.isfile(f):
                        print 'Encoding file %s' %f
                        encode_mp3(os.path.join(root,x), f)
                        #we only want to encode one file at a time as the synology NAS is very very slow so we dont wanna lock it up forever
                        sys.exit()



if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-r', '--remove', help='removes non flac files and empty folders from source', dest='remove', default=False, action='store_true')
    (opts, args) = parser.parse_args()
    if len(args) != 2:
        print 'usage: %s <source dir> <target dir>' % (sys.argv[0])
        sys.exit(1)

    main(opts , sys.argv[1:])