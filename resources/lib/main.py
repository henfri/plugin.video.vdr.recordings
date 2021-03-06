# -*- coding: utf-8 -*-
# Copyright: GNU GPLv3
# pylint: disable=E0401
# Disable import error: E0401

import os
import urlparse
import string
import xbmcgui
import xbmcplugin
import xbmc
import xbmcaddon
import constants

from vdrrecordingfolder import VdrRecordingFolder
from bookmarks import bookmarks
import kfolder

    
def GUIEditExportName(name):
    kb = xbmc.Keyboard('', name, True)
    kb.setHiddenInput(False)
    kb.doModal()
    if kb.isConfirmed():
      name = kb.getText()
      return name
    else:
      return None


class main:
    def __init__(self, argv):
        self.argv = argv
        self.base_url = self.argv[0]
        self.addon_handle = int(self.argv[1])
        self.args = urlparse.parse_qs(self.argv[2][1:])
        self.mode = self.args.get('mode', ['folder'])[0]
        addon = xbmcaddon.Addon('plugin.video.vdr.recordings')
        self.rootFolder = addon.getSetting("rootFolder")
        if not os.path.isdir(self.rootFolder):
            xbmc.executebuiltin('Notification(Folder ' + self.rootFolder +
           ' does not exist.,Please select correct video folder in stettings., 50000)')
        lastChar = self.rootFolder[-1] 
        if lastChar == '/' or lastChar == '\\':
           self.rootFolder = self.rootFolder[:-1]
        if self.addon_handle > 0:
            xbmcplugin.setContent(self.addon_handle, 'movies')

    def modeFolder(self):
        currentFolder = self.args.get('currentFolder', [self.rootFolder])[0]
        kf = kfolder.kFolder(currentFolder)
        kf.parseFolder(self.addon_handle, self.base_url, self.rootFolder)
# Add special (search) folder
#        url = self.build_url({'mode': 'search', 'currentFolder': currentFolder})
#        li = xbmcgui.ListItem(" search", iconImage = 'DefaultFolder.png')
#        xbmcplugin.addDirectoryItem(handle=self.addon_handle, url=url,
#                                listitem=li, isFolder=True)

    def doSearch(self, searchString):
#        currentFolder = self.args.get('currentFolder', [self.rootFolder])[0]
# Add special (search) folder
#        url = self.build_url({'mode': 'search', 'currentFolder': currentFolder})
#        li = xbmcgui.ListItem(" search", iconImage = 'DefaultFolder.png')
#        xbmcplugin.addDirectoryItem(handle=self.addon_handle, url=url,
#                                listitem=li, isFolder=True)
        searchList = []
        for dirName, subdirList, fileList in os.walk(self.rootFolder, followlinks = True):
            if dirName[-4:] == ".rec":
                searchList.append(VdrRecordingFolder(dirName))

        searchStringL = string.lower(searchString)
        for vdrRecordingFolder in searchList:
            if string.find(string.lower(vdrRecordingFolder.title), searchStringL) >= 0:
                relRecordingPath = os.path.split(vdrRecordingFolder.path)[0][len(self.rootFolder)+1:].replace('_', ' ')
                vdrRecordingFolder.description = relRecordingPath + '\n' + vdrRecordingFolder.description
# add context menu
                commands = []
                kfolder.addContextMenuCommand(commands, "Delete", constants.DELETE, vdrRecordingFolder.path)
                vdrRecordingFolder.addDirectoryItem(self.addon_handle, commands)                                
        xbmcplugin.addSortMethod(self.addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.addSortMethod(self.addon_handle, xbmcplugin.SORT_METHOD_DATEADDED)
        xbmcplugin.endOfDirectory(self.addon_handle)

    def modeSearch(self):
        searchStringx = self.args.get('searchString', [''])[0]
        self.doSearch(searchStringx)

    def modeSearch2(self):
        searchStringx = GUIEditExportName("Enter search string")
        if (searchStringx == None):
            self.modeFolder()
        else:
#           xbmc.log("searchString " + str(searchStringx), xbmc.LOGERROR)
            self.doSearch(searchStringx)

