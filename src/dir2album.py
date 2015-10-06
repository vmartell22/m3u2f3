#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import os
import sys
import getopt
import hashlib
import shutil
import traceback
import glob
from mutagen import id3, File, m4a, aiff

def _usage():
    s_help = "Usage:  dir2album source_directory target_directory\n"
    s_help += "Options:\n"
    s_help += "\n%5s,\t%s\t\t\t%s\n\n" % ("-h", "--help", "display this help and exit")

    print s_help


def ProcessDirectory(ps_SourcePath="", ps_TargetPath="./"):

    # Loading Playlist
    MUSIC_FILES = os.listdir(ps_SourcePath)

    # Let's rock
    for s_MusicFile in MUSIC_FILES:

        s_FullFile = os.path.abspath( "%s/%s" %(ps_SourcePath,s_MusicFile) )
        print "Processing: %s" %( s_FullFile)
        s_Name, s_Ext = os.path.splitext(s_FullFile)

        try:

            s_Album         = ""
            bin_coverArt    = None

            if s_Ext == ".m4a":

                m4a_fullFile = m4a.M4A(s_FullFile)
                s_Album = m4a_fullFile['\xa9alb'].encode("utf-8", "ignore")
                bin_coverArt  = m4a_fullFile['covr']

            elif s_Ext == ".mp3":

                id3_fullFile = id3.ID3(s_FullFile)
                s_Album = id3_fullFile['TALB'].text[0]
                for k,v in id3_fullFile.items():
                    if k.startswith("APIC"):
                        s_key=k
                        break
                bin_coverArt  = id3_fullFile[s_key].data

            elif s_Ext == ".aif":

                id3_fullFile = aiff.AIFF(s_FullFile)
                s_Album = id3_fullFile.tags['TALB'].text[0]
                for k,v in id3_fullFile.tags.items():
                    if k.startswith("APIC"):
                        s_key=k
                        break
                bin_coverArt  = id3_fullFile.tags[s_key].data

            elif s_Ext == ".dsf":
                continue
            else:
                print "Unknown extension!!!"
                print s_fullFile
                exit()


            s_TargetDir = "%s/%s" % (ps_TargetPath,hashlib.md5(s_Album).hexdigest())

            print "Album: %s Targedir: %s" %(s_Album,s_TargetDir)

            # New dir ?
            if not os.path.exists(s_TargetDir):
                os.makedirs(s_TargetDir)
                with open("%s/folder.jpg"%(s_TargetDir), 'wb') as file_coverArt:
                    file_coverArt.write(bin_coverArt)
            shutil.copy2( s_FullFile , "%s/"%(s_TargetDir) )


        except (shutil.Error, IOError) as e:

            print "Failed to process: %s - New File: %s" %(s_FullFile,s_NewFilename)
            print(traceback.format_exc())



if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.stderr.write("Missing Parameters\n")
        sys.exit(1)

    s_Options = "h"
    s_LongOptions = ["help"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], s_Options, s_LongOptions)

    except getopt.GetoptError:
        print "Invalid parameters"
        _usage()
        sys.exit(2)

    s_PlayList = ""
    s_TargetPath = "./"

    # Process parameters
    for o, a in opts:
        if o in ("-h", "--help"):
            _usage()
            sys.exit(1)

    try:
        s_SourcePath = args[0]
    except:
        pass

    try:
        s_TargetPath = args[1]
    except:
        pass

    print "Processing Directory: %s to Target Path: %s" %(s_SourcePath, s_TargetPath)

    if os.path.exists(s_TargetPath) and os.path.exists(s_SourcePath):
        ProcessDirectory(s_SourcePath, s_TargetPath)

    else:
        sys.stderr.write("A Provided Path does not exist..\n")
        sys.exit(2)
