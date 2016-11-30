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
from mutagen import id3, File, m4a, aiff, mp4


def _usage():
    s_help = "Usage: extract_cover [working directory]\n"
    s_help += "Options:\n"
    s_help += "\n%5s,\t%s\t\t\t%s\n\n" % ("-h", "--help", "display this help and exit")

    print s_help


def processCover(ps_TargetPath, ps_MusicFile):

    # Let's rock
    s_FullFile = "%s/%s"%(ps_TargetPath,ps_MusicFile)
    print "Analyzing: %s" %(s_FullFile)
    s_Name, s_Ext = os.path.splitext(s_FullFile)
    _, s_Name = os.path.split(s_Name)
    b_gotCover = False

    try:

        s_Album         = ""
        bin_coverArt    = None
        s_coverArtType  = "jpg"

        if s_Ext == ".m4a" or s_Ext == ".mp4":

            m4a_fullFile = mp4.MP4(s_FullFile)
            s_Album = m4a_fullFile.tags['\xa9alb'][0]

            if 'covr' in m4a_fullFile.tags:
                bin_coverArt  = m4a_fullFile['covr'][0]
                if m4a_fullFile['covr'][0].imageformat == m4a.M4ACover.FORMAT_PNG:
                    s_coverArtType = "png"

        elif s_Ext == ".mp3":

            id3_fullFile = id3.ID3(s_FullFile)
            s_Album = id3_fullFile['TALB'].text[0]
            for k,v in id3_fullFile.items():
                if k.startswith("APIC"):
                    bin_coverArt  = id3_fullFile[k].data
                    if "png" in id3_fullFile[k].mime:
                        s_coverArtType = "png"
                    break

        elif s_Ext == ".aif" or s_Ext == ".aiff":

            id3_fullFile = aiff.AIFF(s_FullFile)
            s_Album = id3_fullFile.tags['TALB'].text[0]
            for k,v in id3_fullFile.tags.items():
                if k.startswith("APIC"):
                    bin_coverArt  = id3_fullFile.tags[k].data
                    if "png" in id3_fullFile[k].mime:
                        s_coverArtType = "png"
                    break

        elif s_Ext == ".dsf":
            print "Ignoring DSF extension"
        else:
            print "Unknown extension for file %s at %s" %(ps_MusicFile,ps_TargetPath)

        if bin_coverArt is not None:
            with open("%s/cover.%s"%(ps_TargetPath,s_coverArtType), 'wb') as file_coverArt:
                file_coverArt.write(bin_coverArt)
            b_gotCover = True
        else:
            print "No cover in to process in: %s" %(s_FullFile)

        return b_gotCover

    except (shutil.Error, IOError) as e:

        print "Failed to process: %s" %(s_FullFile)
        print(traceback.format_exc())



# Directory processing
def ProcessDirectory(ps_TargetPath="./"):

    # files in directory
    MUSIC_FILES = os.listdir(ps_TargetPath)

    # We only process the first file to extract the cover - we
    # are assuming that the rest of the files will have the same cover

    coverProcessed = False
    # Let's rock
    for s_MusicFile in MUSIC_FILES:

        s_FullMusicFile = "%s/%s"%(ps_TargetPath,s_MusicFile)
        if os.path.isfile(s_FullMusicFile)  and not coverProcessed and not s_MusicFile.startswith('.'):

            print "Processing %s" %(s_FullMusicFile)
            if processCover(ps_TargetPath, s_MusicFile):
                print "Extracted Cover From File: %s at Targedir: %s" %(s_MusicFile, ps_TargetPath)
                coverProcessed = True
            else:
                print "Fail To Extract Cover From File: %s at Targedir: %s - Trying Next File" %(s_MusicFile, ps_TargetPath)

        elif os.path.isdir(s_FullMusicFile):

            # Process directory
            ProcessDirectory(s_FullMusicFile)

    return


# Main
if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.stderr.write("Missing  Parameters\n")
        sys.exit(1)

    s_Options = "h"
    s_LongOptions = ["help"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], s_Options, s_LongOptions)

    except getopt.GetoptError:
        print "Invalid parameters"
        _usage()
        sys.exit(2)

    s_TargetPath = "./"

    # Process parameters
    for o, a in opts:
        if o in ("-h", "--help"):
            _usage()
            sys.exit(1)

    try:
        s_TargetPath = args[0]
    except:
        pass

    print "Processing Target Path: %s" % (s_TargetPath)

    if os.path.exists(s_TargetPath):
        ProcessDirectory(s_TargetPath)

    else:
        sys.stderr.write("A Provided Path does not exist..\n")
        sys.exit(2)
