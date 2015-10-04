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
import ID3


def _usage():
    s_help = "Usage:  m3u2f3 playlist_name target_directory\n"
    s_help += "Options:\n"
    s_help += "\n%5s,\t%s\t\t\t%s\n\n" % ("-h", "--help", "display this help and exit")

    print s_help


def ProcessPlayList(ps_PlayList="", ps_TargetPath="./"):

    # Loading Playlist
    with open(ps_PlayList) as INF:
        MUSIC_FILES = [LINE.strip() for LINE in INF.readlines() if not LINE.startswith('#')]

    # Let's rock
    for s_MusicFile in MUSIC_FILES:


        s_FullFile = os.path.abspath( s_MusicFile )
        print "Processing: %s" %( s_FullFile)
        s_Name, s_Ext = os.path.splitext(s_FullFile)
        s_Name = os.path.basename(s_Name)
        s_NewFilename = "%s%s" %(hashlib.md5(s_FullFile).hexdigest(),s_Ext)
        print "Process Name: %s/%s" %(ps_TargetPath,s_Name)
        print "New Filename: %s" %(s_NewFilename)

        try:

            # New dir ?
            id3_fullFile = ID3(s_FullFile)
            pprint.pprint(id3_full_file)
            s_TargetDir = "%s/%s" % (ps_TargetPath,id3_fullFile['ALBUM'])

            if not os.path.exists(directory):
                os.makedirs(directory)


            shutil.copy2( s_FullFile , "%s/"%(ps_TargetPath) )
            os.rename( "%s/%s%s"%(ps_TargetPath,s_Name,s_Ext),  "%s/%s"%(ps_TargetPath,s_NewFilename)  )

        except (shutil.Error, IOError) as e:

            print "Failed to process: %s - New File: %s" %(s_FullFile,s_NewFilename)
            print(traceback.format_exc())
            pass



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
        s_PlayList = args[0]
    except:
        pass

    try:
        s_TargetPath = args[1]
    except:
        pass

    print "Processing Playlist: %s Target Path: %s" %(s_PlayList, s_TargetPath)

    if os.path.exists(s_TargetPath) and os.path.isfile(s_PlayList):
        ProcessPlayList(s_PlayList, s_TargetPath)

    else:
        sys.stderr.write("A Provided Path does not exist..\n")
        sys.exit(2)
